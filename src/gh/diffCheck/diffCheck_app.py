#! python3

import System
import typing



import sys

# # Get the directory containing the script file
# script_dir = os.path.dirname(os.path.realpath(__file__))

# # Construct absolute paths
# path1 = os.path.join(script_dir, "src", "gh", "diffCheck", "diffCheck")
# path2 = os.path.join(script_dir, "src", "gh", "diffCheck")

# # Add the paths to sys.path
# sys.path.append(path1)
# sys.path.append(path2)

# # for p in sys.path:
# #     print(p)

# # modules = [diffCheck, diffCheck.df_cvt_bindings]
# # for module in modules:
# #     importlib.reload(module)

# # packages_2_reload = ["diffCheck"]

# # if packages_2_reload is not None:
# #     if packages_2_reload.__len__() != 0:
# #         print("Reloading packages")
# #         for package in packages_2_reload:
# #             for key in list(sys.modules.keys()):
# #                 if package in key:
# #                     print(sys.modules[key])
# #                     #check that the package must have the attribute __path__
# #                     if hasattr(sys.modules[key], '__file__'):
# #                         print(sys.modules[key])
# #                         importlib.reload(sys.modules[key])

# import Rhino
# import Rhino.Geometry as rg
# from ghpythonlib.componentbase import executingcomponent as component

# import Grasshopper as gh
# from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

# import diffCheck
# from diffCheck import diffcheck_bindings
# import diffCheck.df_geometries
# import diffCheck.df_cvt_bindings





# class DFMeshToCloud(component):
#     def RunScript(self,
#             i_mesh: rg.Mesh,
#             i_points: int) -> rg.PointCloud:
#         """
#             Convert a Rhino mesh to a cloud.

#             :param i_mesh: mesh to convert
#             :param i_points: number of points to sample

#             :return o_cloud: rhino cloud
#         """


#         diffCheck.df_cvt_bindings.test()
#         # diffCheck.df_geometries.test()


#         df_mesh = diffCheck.df_cvt_bindings.cvt_rhmesh_2_dfmesh(i_mesh)
#         df_cloud = df_mesh.sample_points_uniformly(i_points)

#         # convert the df_cloud to a rhino cloud
#         rgpoints = [rg.Point3d(pt[0], pt[1], pt[2]) for pt in df_cloud.points]
#         rh_cloud = rg.PointCloud(rgpoints)

#         return [rh_cloud]


if __name__ == "__main__":
    # com = DFMeshToCloud()
    # com.RunScript(i_mesh, i_points)
    print("test")