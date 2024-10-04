#! python3
"""
    This module contains the utility functions to compute the difference between source and target
"""

import typing
from enum import Enum

import numpy as np

import Rhino
import Rhino.Geometry as rg

from diffCheck import diffcheck_bindings  # type: ignore
from diffCheck import df_cvt_bindings
from diffCheck.df_geometries import DFAssembly


class DFInvalidData(Enum):
    """
    Enum to define the type of invalid data for joint or assembly analysis
    """
    # healty data
    VALID = 0
    # the joint or  beam is way to out of the tolerance established in the joint/assembly segmentator
    OUT_OF_TOLERANCE = 1
    # we are missing scan points to evaluate
    MISSING_PCD = 2

class DFVizResults:
    """
    This class compiles the resluts of the error estimation into one object
    """

    def __init__(self, assembly):

        self.source = []
        self.target = []

        self.distances_mean = []
        self.distances_rmse = []
        self.distances_max_deviation = []
        self.distances_min_deviation = []
        self.distances_sd_deviation = []
        self.distances = []
        self.assembly = assembly

        self.sanity_check = []

        self._is_source_cloud = True  # if False it's a mesh

    def add(self, source, target, distances, sanity_check: DFInvalidData = DFInvalidData.VALID):

        self.source.append(source)
        self.target.append(target)

        self.sanity_check.append(sanity_check)

        if sanity_check == DFInvalidData.OUT_OF_TOLERANCE:
            self.distances_mean.append(DFInvalidData.OUT_OF_TOLERANCE)
            self.distances_rmse.append(DFInvalidData.OUT_OF_TOLERANCE)
            self.distances_max_deviation.append(DFInvalidData.OUT_OF_TOLERANCE)
            self.distances_min_deviation.append(DFInvalidData.OUT_OF_TOLERANCE)
            self.distances_sd_deviation.append(DFInvalidData.OUT_OF_TOLERANCE)
            self.distances.append(distances.tolist())
        elif sanity_check == DFInvalidData.MISSING_PCD:
            self.distances_mean.append(DFInvalidData.MISSING_PCD)
            self.distances_rmse.append(DFInvalidData.MISSING_PCD)
            self.distances_max_deviation.append(DFInvalidData.MISSING_PCD)
            self.distances_min_deviation.append(DFInvalidData.MISSING_PCD)
            self.distances_sd_deviation.append(DFInvalidData.MISSING_PCD)
            self.distances.append(np.empty(0))
        else:
            self.distances_mean.append(np.mean(distances))
            self.distances_rmse.append(np.sqrt(np.mean(distances ** 2)))
            self.distances_max_deviation.append(np.max(distances))
            self.distances_min_deviation.append(np.min(distances))
            self.distances_sd_deviation.append(np.std(distances))
            self.distances.append(distances.tolist())

    def filter_values_based_on_valuetype(self, settings):

        if settings.valueType == "Dist":
            valid_sublists = [sublist for sublist in self.distances if len(sublist) > 0]
            min_value = min(min(sublist) for sublist in valid_sublists)
            max_value = max(max(sublist) for sublist in valid_sublists)
            values = self.distances

        elif settings.valueType == "MEAN":
            valid_values = [value for value in self.distances_mean if value is not None]
            min_value = min(valid_values)
            max_value = max(valid_values)
            values = self.distances_mean

        elif settings.valueType == "RMSE":
            valid_values = [value for value in self.distances_rmse if value is not None]
            min_value = min(valid_values)
            max_value = max(valid_values)
            values = self.distances_rmse

        elif settings.valueType == "MAX":
            valid_values = [value for value in self.distances_max_deviation if value is not None]
            min_value = min(valid_values)
            max_value = max(valid_values)
            values = self.distances_max_deviation

        elif settings.valueType == "MIN":
            valid_values = [value for value in self.distances_min_deviation if value is not None]
            min_value = min(valid_values)
            max_value = max(valid_values)
            values = self.distances_min_deviation

        elif settings.valueType == "STD":
            valid_values = [value for value in self.distances_sd_deviation if value is not None]
            min_value = min(valid_values)
            max_value = max(valid_values)
            values = self.distances_sd_deviation

        # threshold values
        if settings.lower_threshold is not None:
            min_value = settings.lower_threshold
        if settings.upper_threshold is not None:
            max_value = settings.upper_threshold

        return values, min_value, max_value

    @property
    def is_source_cloud(self):
        return type(self.source[0]) is diffcheck_bindings.dfb_geometry.DFPointCloud


def df_cloud_2_df_cloud_comparison(source_list, target_list):
    """
        Compute the Euclidean distance for every point of a source pcd to its
        closest point on a target pointcloud
    """
    results = DFVizResults(DFAssembly())
    for source, target in zip(source_list, target_list):
        distances = np.asarray(source.compute_distance(target))
        results.add(source, target, distances)

    return results


def rh_cloud_2_rh_mesh_comparison(
    assembly: DFAssembly,
    rh_cloud_source_list: typing.List[Rhino.Geometry.PointCloud],
    rhino_mesh_target_list: typing.List[rg.Mesh],
    signed_flag: bool,
    swap: bool,
    ) -> DFVizResults:
    """
        Computes distances between a pcd and a mesh and return the results

        :param assembly: the DFAssembly object
        :param rh_cloud_source_list: list of point clouds after segmentation in Rhino format
        :param rhino_mesh_target_list: list of rhino meshes
        :param signed_flag: flag to compute signed distances
        :param swap: this mean we want to visualize the result on the target mesh (or viceversa)

        :return: the results of the comparison
    """
    results = DFVizResults(assembly)

    for idx, source_rh in enumerate(rh_cloud_source_list):
        source_df = df_cvt_bindings.cvt_rhcloud_2_dfcloud(source_rh)
        target = rhino_mesh_target_list[idx]

        source_df_pts = source_df.points

        if swap:
            source_df, target = target, source_df

        # FIXME: this is a hack to avoid that the assembly segmentator breaks this
        # snippet because it is not stamping the rhino pout cloud with the sanity check
        # user string value.
        sanity_check_value_uncasted = source_rh.GetUserString("df_sanity_scan_check")
        sanity_check_value = None
        if sanity_check_value_uncasted is None:
            sanity_check_value = DFInvalidData.VALID.value
        else:
            sanity_check_value = int(sanity_check_value_uncasted)

        if sanity_check_value == DFInvalidData.OUT_OF_TOLERANCE.value:
            out_of_tol_distances = np.asarray([DFInvalidData.OUT_OF_TOLERANCE] * len(source_df_pts))
            results.add(source_df, target, out_of_tol_distances, sanity_check=DFInvalidData.OUT_OF_TOLERANCE)
        elif sanity_check_value == DFInvalidData.MISSING_PCD.value or len(source_df_pts) == 0:
            results.add(source_df, target, np.empty(0), sanity_check=DFInvalidData.MISSING_PCD)
        else:
            if swap:
                # this mean we want to visualize the result on the target mesh
                distances = rh_mesh_2_df_cloud_distance(source_df, target, signed_flag)
            else:
                # this means we want to visualize the result on the source pcd
                distances = df_cloud_2_rh_mesh_distance(source_df, target, signed_flag)
            results.add(source_df, target, distances)

    return results

def rh_mesh_2_df_cloud_distance(source, target, signed=False):
    """
        Calculate the distance between every vertex of a Rhino Mesh to its closest point on a PCD
    """
    # make a Df point cloud containing all the vertices of the source rhino mesh
    df_pcd_from_mesh_vertices = diffcheck_bindings.dfb_geometry.DFPointCloud()
    df_pcd_from_mesh_vertices.points = [[pt.X, pt.Y, pt.Z] for pt in source.Vertices]

    # calculate the distances
    distances = np.asarray(df_pcd_from_mesh_vertices.compute_distance(target))

    if signed:
        # build an RTree containing all the points of the target
        tree = rg.RTree()
        for i, ver in enumerate(target.points):
            tree.Insert(rg.Point3d(ver[0], ver[1], ver[2]), i)

        for idx, p in enumerate(source.Vertices):
            # find the index on the target that the vertex is closest to
            search_point = p
            sphere = rg.Sphere(search_point, distances[idx]*1.0001) #to change later, hack to avoid not finding the point
            found_indices = []

            def search_callback(sender, e):
                found_indices.append(e.Id)

            tree.Search(sphere, search_callback)

            df_closest_point = target.points[found_indices[0]]
            closest_point = rg.Point3d(df_closest_point[0], df_closest_point[1], df_closest_point[2])
            # Calculate the direction from target to source
            direction = p - closest_point
            # Calculate the signed distance
            normal = source.Normals[idx]
            dot_product = direction * normal
            if dot_product < 0:
                distances[idx] = - distances[idx]

    return np.asarray(distances)


def df_cloud_2_rh_mesh_distance(source, target, signed=False):
    """
        Calculate the distance between every point of a source pcd to its closest point on a target Rhino Mesh
    """

    #for every point on the point cloud find distance to mesh
    distances = []

    for p in source.points:

        rhp = rg.Point3d(p[0], p[1], p[2])
        closest_meshPoint = target.ClosestMeshPoint(rhp, 1000)
        closest_point = closest_meshPoint.Point
        distance = rhp.DistanceTo(closest_point)

        if signed:
            # Calculate the direction from target to source
            direction = rhp - closest_point
            # Calculate the signed distance
            normal = target.NormalAt(closest_meshPoint)
            dot_product = direction * normal
            if dot_product < 0:
                distance = -distance

        distances.append(distance)

    return np.asarray(distances)
