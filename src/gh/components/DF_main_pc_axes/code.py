#! python3

from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings
from diffCheck import df_poses

import Rhino

from ghpythonlib.componentbase import executingcomponent as component
# from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

import System

def compute_dot_product(v1, v2):
    """
    Compute the dot product of two vectors.
    """
    return v1.X * v2.X + v1.Y * v2.Y + v1.Z * v2.Z

class DFMainPCAxes(component):
    def RunScript(self,
            i_clouds: System.Collections.Generic.List[Rhino.Geometry.PointCloud],
            i_file_name: str,
            reset: bool) -> System.Collections.Generic.IList[Rhino.Geometry.Vector3d]:

        planes = []
        all_poses_in_time = df_poses.DFPosesAssembly()
        if reset:
            all_poses_in_time.reset()
            return None, None

        previous_poses = all_poses_in_time.get_last_poses()
        all_poses_this_time = []
        for i, cloud in enumerate(i_clouds):
            df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(cloud)
            if df_cloud is None:
                return None, None
            df_cloud.estimate_normals(True, 12)

            # hint = df_cvt_bindings.cvt_dfcloud_2_rhcloud(df_cloud)
            df_points = df_cloud.get_axis_aligned_bounding_box()
            df_point = (df_points[0] + df_points[1]) / 2
            rh_point = Rhino.Geometry.Point3d(df_point[0], df_point[1], df_point[2])
            vectors = []
            # Get the main axes of the point cloud
            previous_pose = previous_poses[i] if previous_poses else None
            if previous_pose:
                rh_previous_xDirection = Rhino.Geometry.Vector3d(previous_pose.xDirection[0], previous_pose.xDirection[1], previous_pose.xDirection[2])
                rh_previous_yDirection = Rhino.Geometry.Vector3d(previous_pose.yDirection[0], previous_pose.yDirection[1], previous_pose.yDirection[2])
            n_faces = len(diffcheck_bindings.dfb_segmentation.DFSegmentation.segment_by_normal(df_cloud, 12, int(len(df_cloud.points)/20), True, int(len(df_cloud.points)/200), 1))
            axes = df_cloud.get_principal_axes(n_faces)
            for axe in axes:
                vectors.append(Rhino.Geometry.Vector3d(axe[0], axe[1], axe[2]))
            if previous_pose:
                # Sort the vectors by their alignment with the previous xDirection and yDirection
                sorted_vectors_by_alignment = sorted(vectors, key=lambda v: compute_dot_product(v, rh_previous_xDirection), reverse=True)
                sorted_vectors_by_perpendicularity = sorted(vectors, key=lambda v: compute_dot_product(v, rh_previous_yDirection), reverse=True)
                new_xDirection = sorted_vectors_by_alignment[0]
                new_yDirection = sorted_vectors_by_perpendicularity[0] #- compute_dot_product(sorted_vectors_by_perpendicularity[0], new_xDirection) * new_xDirection
                new_yDirection.Unitize()
            else:
                # If no previous pose, just use the first two vectors as x and y directions
                new_xDirection = vectors[0]
                new_yDirection = vectors[1] #- compute_dot_product(vectors[1], new_xDirection) * new_xDirection
                new_yDirection.Unitize()

            print(new_xDirection)
            print(new_yDirection)

            pose = df_poses.DFPose(
                origin = [rh_point.X, rh_point.Y, rh_point.Z],
                xDirection = [new_xDirection.X, new_xDirection.Y, new_xDirection.Z],
                yDirection = [new_yDirection.X, new_yDirection.Y, new_yDirection.Z])
            all_poses_this_time.append(pose)
            plane = Rhino.Geometry.Plane(origin = rh_point, xDirection=new_xDirection, yDirection=new_yDirection)
            planes.append(plane)

        all_poses_in_time.add_step(all_poses_this_time)

        return planes, all_poses_in_time.poses_per_element_dictionary


# if __name__ == "__main__":
#     i_file_name = "C:/Users/localuser/test_file_poses.json"
#     component = DFMainPCAxes()
#     if reset == None: # noqa: E711
#         reset = False

#     a, dico = component.RunScript(x, i_file_name, reset) # noqa: F821
