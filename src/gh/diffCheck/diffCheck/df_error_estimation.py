#! python3
"""
    This module contains the utility functions to compute the difference between source and target
"""

import typing
from enum import Enum
from datetime import datetime
import os

import json

import numpy as np

import Rhino
import Rhino.Geometry as rg
from Rhino.FileIO import SerializationOptions

from diffCheck import diffcheck_bindings  # type: ignore
from diffCheck import df_cvt_bindings
from diffCheck.df_geometries import DFAssembly


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy ndarray types. """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, Enum):
            return obj.value  # or use obj.name if you prefer
        return super().default(obj)

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
    This class compiles the results of the error estimation into one object
    """
    __serial_file_extenion: str = ".diffCheck"

    def __init__(self, assembly):

        self.assembly: DFAssembly = assembly
        self.source: typing.List[diffcheck_bindings.dfb_geometry.DFPointCloud] = []
        self.target: typing.List[Rhino.Geometry.Mesh] = []

        self.sanity_check: typing.List[DFInvalidData] = []
        self._is_source_cloud = True  # if False it's a mesh

        self.distances_mean = []
        self.distances_rmse = []
        self.distances_max_deviation = []
        self.distances_min_deviation = []
        self.distances_sd_deviation = []
        self.distances = []

        self._analysis_type: str = None

    def __repr__(self):
        return f"DFVizResults of({self.assembly})"

    def __getstate__(self):
        state = self.__dict__.copy()
        if "assembly" in state and state["assembly"] is not None:
            state["assembly"] = self.assembly.__getstate__()
        if "source" in state and state["source"] is not None:
            state["source"] = [df_cvt_bindings.cvt_dfcloud_2_dict(pcd) for pcd in state["source"]]
        if "target" in state and state["target"] is not None:
            state["target"] = [mesh.ToJSON(SerializationOptions()) for mesh in state["target"]]
        if "sanity_check" in state and state["sanity_check"] is not None:
            state["sanity_check"] = [s.value if isinstance(s, DFInvalidData) else s for s in self.sanity_check]
        return state

    def __setstate__(self, state: typing.Dict):
        if "assembly" in state and state["assembly"] is not None:
            assembly = DFAssembly.__new__(DFAssembly)
            assembly.__setstate__(state["assembly"])
            state["assembly"] = assembly
        if "source" in state and state["source"] is not None:
            source = []
            for pcd_dict in state["source"]:
                pcd = diffcheck_bindings.dfb_geometry.DFPointCloud()
                pcd = df_cvt_bindings.cvt_dict_2_dfcloud(pcd_dict)
                source.append(pcd)
            state["source"] = source
        if "target" in state and state["target"] is not None:
            target = []
            for mesh_json in state["target"]:
                mesh = rg.Mesh()
                mesh = mesh.FromJSON(mesh_json)
                target.append(mesh)
            state["target"] = target
        if "sanity_check" in state and state["sanity_check"] is not None:
            state["sanity_check"] = [DFInvalidData(s) for s in state["sanity_check"]]
        self.__dict__.update(state)

    def dump_serialization(self, dir: str) -> str:
        """ Dump the results into a JSON file for serialization """
        if not os.path.exists(os.path.dirname(dir)):
            try:
                os.makedirs(os.path.dirname(dir))
            except OSError as exc:
                raise exc

        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        assembly_name: str = self.assembly.name
        result_type: str = self.analysis_type
        serial_file_path = os.path.join(dir, f"{assembly_name}_{result_type}_{timestamp}{self.__serial_file_extenion}")

        try:
            with open(serial_file_path, "w") as f:
                json.dump(self.__getstate__(), f, cls=NumpyEncoder)
        except Exception as e:
            raise e

        return serial_file_path

    @staticmethod
    def load_serialization(file_path: str) -> 'DFVizResults':
        """ Load the results from a JSON file """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        if not file_path.endswith(DFVizResults.__serial_file_extenion):
            raise ValueError(f"File {file_path} is not a valid diffCheck file")
        try:
            with open(file_path, "r") as f:
                state = json.load(f)
                obj = DFVizResults.__new__(DFVizResults)
                obj.__setstate__(state)
        except Exception as e:
            raise e
        return obj

    def _compute_dfresult_type(self):
        """
            Detect if the DFVizResults object contains results of beam, joint of joint_face level analysis
        """
        # check that source and target have the same length
        if len(self.source) != len(self.target):
            raise ValueError("Source and target have different length, cannot determine the type of analysis")
        if len(self.assembly.beams) == len(self.source):
            self._analysis_type = "beam"
        elif len(self.assembly.all_joints) == len(self.source):
            self._analysis_type = "joint"
        elif len(self.assembly.all_joint_faces) == len(self.source):
            self._analysis_type = "joint_face"
        return self._analysis_type

    def find_id(self, idx: int,) -> str:
        """
            Return the ID in str format of the element. This func is used during
            the csv export. With the following format:
            - beam: idx
            - joint: idx_b--idx_j--0
            - joint_face: idx_b--idx_j--idx_f

            :param idx: the index of the element
        """
        counter = 0

        if self.analysis_type == "beam":
            return str(idx)
        elif self.analysis_type == "joint":
            for idx_b, beam in enumerate(self.assembly.beams):
                for idx_j, joint in enumerate(beam.joints):
                    if counter == idx:
                        return f"{idx_b}--{idx_j}--{0}"
                    counter += 1
        elif self.analysis_type == "joint_face":
            for idx_b, beam in enumerate(self.assembly.beams):
                for idx_j, joint in enumerate(beam.joints):
                    for idx_f, face in enumerate(joint.faces):
                        if counter == idx:
                            return f"{idx_b}--{idx_j}--{idx_f}"
                        counter += 1
        return ""

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

    @property
    def analysis_type(self):
        self._analysis_type = self._compute_dfresult_type()
        return self._analysis_type

# FIXME: ths is currently broken, we need to fix it
def df_cloud_2_df_cloud_comparison(
    assembly: DFAssembly,
    df_cloud_source_list: typing.List[diffcheck_bindings.dfb_geometry.DFPointCloud],
    df_cloud_target_list: typing.List[diffcheck_bindings.dfb_geometry.DFPointCloud]
    ) -> DFVizResults:
    """
        Compute the Euclidean distance for every point of a source pcd to its
        closest point on a target pointcloud
    """
    results = DFVizResults(
        DFAssembly(
            [], "cloud-cloud-dummy-dfassembly"
        ))
    for source, target in zip(df_cloud_source_list, df_cloud_target_list):
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
