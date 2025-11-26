"""This compoment calculates the pose of a data tree of point clouds."""
#! python3

from diffCheck import df_cvt_bindings
from diffCheck import df_poses
from diffCheck.diffcheck_bindings import dfb_geometry

import Rhino
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
import Grasshopper
import ghpythonlib.treehelpers as th

from ghpythonlib.componentbase import executingcomponent as component


class DFPoseEstimation(component):
    def RunScript(self,
            i_face_clouds: Grasshopper.DataTree[Rhino.Geometry.PointCloud],
            i_assembly,
            i_reset: bool,
            i_save: bool):

        clusters_per_beam = th.tree_to_list(i_face_clouds)
        # ensure assembly has enough beams
        if len(i_assembly.beams) < len(clusters_per_beam):
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Assembly has fewer beams than input clouds")  # noqa: F821
            return None, None

        planes = []
        all_poses_in_time = df_poses.DFPosesAssembly()
        if i_reset:
            all_poses_in_time.reset()
            return None, None

        all_poses_this_time = []
        for i, face_clouds in enumerate(clusters_per_beam):
            try:
                df_cloud = dfb_geometry.DFPointCloud()

                rh_face_normals = []
                for face_cloud in face_clouds:
                    df_face_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(face_cloud)
                    df_cloud.add_points(df_face_cloud)
                    plane_normal = df_face_cloud.fit_plane_ransac()
                    rh_face_normals.append(Rhino.Geometry.Vector3d(plane_normal[0], plane_normal[1], plane_normal[2]))

                df_bb_points = df_cloud.get_axis_aligned_bounding_box()
                df_bb_centroid = (df_bb_points[0] + df_bb_points[1]) / 2
                rh_bb_centroid = Rhino.Geometry.Point3d(df_bb_centroid[0], df_bb_centroid[1], df_bb_centroid[2])

                new_xDirection, new_yDirection = df_poses.select_vectors(rh_face_normals, i_assembly.beams[i].plane.XAxis, i_assembly.beams[i].plane.YAxis)

                pose = df_poses.DFPose(
                    origin = [rh_bb_centroid.X, rh_bb_centroid.Y, rh_bb_centroid.Z],
                    xDirection = [new_xDirection.X, new_xDirection.Y, new_xDirection.Z],
                    yDirection = [new_yDirection.X, new_yDirection.Y, new_yDirection.Z])
                all_poses_this_time.append(pose)
                plane = Rhino.Geometry.Plane(origin = rh_bb_centroid, xDirection=new_xDirection, yDirection=new_yDirection)
                planes.append(plane)

            except Exception as e:
                # Any unexpected error on this cloud, skip it and keep going
                ghenv.Component.AddRuntimeMessage(RML.Error, f"Cloud {i}: processing failed ({e}); skipping.")  # noqa: F821
                planes.append(None)
                all_poses_this_time.append(None)
                continue

        if i_save:
            all_poses_in_time.add_step(all_poses_this_time)

        return [planes, all_poses_in_time.to_gh_tree()]
