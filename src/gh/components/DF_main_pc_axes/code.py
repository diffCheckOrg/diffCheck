#! python3

from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings
from diffCheck import df_poses

import Rhino

from ghpythonlib.componentbase import executingcomponent as component

import System

def compute_dot_product(v1, v2):
    """
    Compute the dot product of two vectors.
    """
    return (v1.X * v2.X) + (v1.Y * v2.Y) + (v1.Z * v2.Z)

class DFMainPCAxes(component):
    def RunScript(self,
            i_clouds: System.Collections.Generic.List[Rhino.Geometry.PointCloud],
            i_reset: bool):

        planes = []
        all_poses_in_time = df_poses.DFPosesAssembly()
        if i_reset:
            all_poses_in_time.reset()
            return None, None

        previous_poses = all_poses_in_time.get_last_poses()
        all_poses_this_time = []
        for i, cloud in enumerate(i_clouds):
            df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(cloud)
            if df_cloud is None:
                return None, None
            df_cloud.estimate_normals(True, 12)

            df_points = df_cloud.get_axis_aligned_bounding_box()
            df_point = (df_points[0] + df_points[1]) / 2
            rh_point = Rhino.Geometry.Point3d(df_point[0], df_point[1], df_point[2])
            vectors = []
            # Get the main axes of the point cloud
            previous_pose = previous_poses[i] if previous_poses else None
            if previous_pose:
                rh_previous_xDirection = Rhino.Geometry.Vector3d(previous_pose.xDirection[0], previous_pose.xDirection[1], previous_pose.xDirection[2])
                rh_previous_yDirection = Rhino.Geometry.Vector3d(previous_pose.yDirection[0], previous_pose.yDirection[1], previous_pose.yDirection[2])
                n_faces = all_poses_in_time.poses_per_element_dictionary[f"element_{i}"].n_faces
            else:
                rh_previous_xDirection = None
                rh_previous_yDirection = None
                n_faces = len(diffcheck_bindings.dfb_segmentation.DFSegmentation.segment_by_normal(df_cloud, 12, int(len(df_cloud.points)/20), True, int(len(df_cloud.points)/200), 1))

            axes = df_cloud.get_principal_axes(n_faces)
            for axe in axes:
                vectors.append(Rhino.Geometry.Vector3d(axe[0], axe[1], axe[2]))

            new_xDirection, new_yDirection = df_poses.select_vectors(vectors, rh_previous_xDirection, rh_previous_yDirection)

            pose = df_poses.DFPose(
                origin = [rh_point.X, rh_point.Y, rh_point.Z],
                xDirection = [new_xDirection.X, new_xDirection.Y, new_xDirection.Z],
                yDirection = [new_yDirection.X, new_yDirection.Y, new_yDirection.Z])
            all_poses_this_time.append(pose)
            plane = Rhino.Geometry.Plane(origin = rh_point, xDirection=new_xDirection, yDirection=new_yDirection)
            planes.append(plane)

        all_poses_in_time.add_step(all_poses_this_time)

        return [planes, all_poses_in_time]
