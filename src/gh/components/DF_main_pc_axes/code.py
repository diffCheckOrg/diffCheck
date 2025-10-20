#! python3

from diffCheck import df_cvt_bindings
from diffCheck import df_poses

import Rhino
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from ghpythonlib.componentbase import executingcomponent as component

import System

class DFMainPCAxes(component):
    def RunScript(self,
            i_clouds: System.Collections.Generic.List[Rhino.Geometry.PointCloud],
            i_assembly,
            i_save: bool,
            i_reset: bool):

        # ensure assembly has enough beams
        if len(i_assembly.beams) < len(i_clouds):
            ghenv.Component.AddRuntimeMessage(RML.Warning, "Assembly has fewer beams than input clouds")  # noqa: F821
            return None, None

        planes = []
        all_poses_in_time = df_poses.DFPosesAssembly()
        if i_reset:
            all_poses_in_time.reset()
            return None, None

        all_poses_this_time = []
        for i, cloud in enumerate(i_clouds):
            try:
                df_cloud = df_cvt_bindings.cvt_rhcloud_2_dfcloud(cloud)
                if df_cloud is None:
                    return None, None
                if not df_cloud.has_normals():
                    ghenv.Component.AddRuntimeMessage(RML.Error, f"Point cloud {i} has no normals. Please compute the normals.")  # noqa: F821

                df_points = df_cloud.get_axis_aligned_bounding_box()
                df_point = (df_points[0] + df_points[1]) / 2
                rh_point = Rhino.Geometry.Point3d(df_point[0], df_point[1], df_point[2])

                axes = df_cloud.get_principal_axes(3)
                vectors = []
                for axe in axes:
                    vectors.append(Rhino.Geometry.Vector3d(axe[0], axe[1], axe[2]))

                new_xDirection, new_yDirection = df_poses.select_vectors(vectors, i_assembly.beams[i].plane.XAxis, i_assembly.beams[i].plane.YAxis)

                pose = df_poses.DFPose(
                    origin = [rh_point.X, rh_point.Y, rh_point.Z],
                    xDirection = [new_xDirection.X, new_xDirection.Y, new_xDirection.Z],
                    yDirection = [new_yDirection.X, new_yDirection.Y, new_yDirection.Z])
                all_poses_this_time.append(pose)
                plane = Rhino.Geometry.Plane(origin = rh_point, xDirection=new_xDirection, yDirection=new_yDirection)
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
