#! python3

import Rhino
from ghpythonlib.componentbase import executingcomponent as component
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

from diffCheck import df_cvt_bindings
import System


class DFBrepToCloud(component):
    def RunScript(self,
            i_breps: System.Collections.Generic.IList[Rhino.Geometry.Brep],
            i_num_points: int):
        self.meshing_parameters = Rhino.Geometry.MeshingParameters.DefaultAnalysisMesh

        mesh_versions = []

        if i_breps is None:
            self.AddRuntimeMessage(RML.Warning, "Please provide a brep to convert to a cloud")
            return None

        for i_brep in i_breps:
            if not isinstance(i_brep, Rhino.Geometry.Brep):
                self.AddRuntimeMessage(RML.Warning, "Please provide a brep to convert to a cloud")
                return None
            meshes = Rhino.Geometry.Mesh.CreateFromBrep(i_brep, self.meshing_parameters)
            for mesh in meshes:
                mesh_versions.append(mesh)

        unified_mesh = mesh_versions[0]
        unified_mesh.Append(mesh_versions)
        unified_mesh.Faces.ConvertQuadsToTriangles()
        df_mesh = df_cvt_bindings.cvt_rhmesh_2_dfmesh(unified_mesh)
        df_cloud = df_mesh.sample_points_uniformly(i_num_points)
        rgpoints = [Rhino.Geometry.Point3d(pt[0], pt[1], pt[2]) for pt in df_cloud.points]
        rh_cloud = Rhino.Geometry.PointCloud(rgpoints)
        print(rh_cloud)
        return [rh_cloud]
