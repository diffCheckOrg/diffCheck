#! python3
"""
    This module contains the utility functions to convert the data between the
    Rhino, the basic diffCheck data structures and the diffCheck bindings.
"""

import Rhino
import Rhino.Geometry as rg
import scriptcontext as sc

from diffCheck import diffcheck_bindings


def cvt_rhcloud_2_dfcloud(rh_cloud) -> diffcheck_bindings.dfb_geometry.DFPointCloud:
    """
        Convert a Rhino cloud to a diffCheck cloud.

        :param rh_cloud: rhino cloud

        :return df_cloud: diffCheck cloud
    """
    if not isinstance(rh_cloud, rg.PointCloud):
        raise ValueError("rh_cloud for convertion should be a PointCloud")

    df_cloud = diffcheck_bindings.dfb_geometry.DFPointCloud()

    # points
    if rh_cloud.Count == 0:
        print("The input rhino cloud is empty")
        return df_cloud
    df_cloud.points = [[pt.X, pt.Y, pt.Z] for pt in rh_cloud]

    # normals
    if rh_cloud.ContainsNormals:
        df_cloud.normals = [[n.X, n.Y, n.Z] for n in rh_cloud.GetNormals()]

    # colors
    if rh_cloud.ContainsColors:
        df_cloud.colors = [c for c in rh_cloud.GetColors()]

    return df_cloud

def cvt_dfcloud_2_rhcloud(df_cloud):
    """
        Convert a diffCheck cloud to a Rhino cloud.

        :param df_cloud: diffCheck cloud

        :return rh_cloud: rhino cloud
    """
    if not isinstance(df_cloud, diffcheck_bindings.dfb_geometry.DFPointCloud):
        raise ValueError("df_cloud should be a DFPointCloud")

    rh_cloud = rg.PointCloud()

    if len(df_cloud.points) == 0:
        print("The input diffCheck cloud is empty")
        return rh_cloud

    df_cloud_points = df_cloud.points
    df_cloud_colors = df_cloud.colors
    df_cloud_normals = df_cloud.normals

    df_cloud_points = [rg.Point3d(pt[0], pt[1], pt[2]) for pt in df_cloud_points]
    df_cloud_normals = [rg.Vector3d(n[0], n[1], n[2]) for n in df_cloud_normals]
    df_cloud_colors = [Rhino.Display.Color4f(c[0], c[1], c[2], 1.0) for c in df_cloud_colors]

    rh_cloud = rg.PointCloud()

    if df_cloud.has_normals() and df_cloud.has_colors():
        rh_cloud.AddRange(df_cloud_points, df_cloud_normals, df_cloud_colors)
    elif df_cloud.has_normals():
        rh_cloud.AddRange(df_cloud_points, df_cloud_normals)
    elif df_cloud.has_colors():
        rh_cloud.AddRange(df_cloud_points, df_cloud_colors)
    else:
        rh_cloud.AddRange(df_cloud_points)

    return rh_cloud

def cvt_dfmesh_2_rhmesh(df_mesh: diffcheck_bindings.dfb_geometry.DFMesh) -> rg.Mesh:
    """
        Convert a diffCheck mesh to a Rhino mesh.

        :param df_mesh: diffCheck mesh

        :return rh_mesh: rhino mesh
    """
    if not isinstance(df_mesh, diffcheck_bindings.dfb_geometry.DFMesh):
        raise ValueError("df_mesh should be a DFMesh")

    rh_mesh = rg.Mesh()

    if len(df_mesh.vertices) == 0:
        print("The input diffCheck mesh is empty")
        return rh_mesh

    # vertices
    for vertex in df_mesh.vertices:
        rh_mesh.Vertices.Add(vertex[0], vertex[1], vertex[2])

    # faces
    for face in df_mesh.faces:
        int_face = [int(f) for f in face]
        rh_mesh.Faces.AddFace(int_face[0], int_face[1], int_face[2])

    # normals
    if len(df_mesh.normals_vertex) > 0:
        for i, normal in enumerate(df_mesh.normals_vertex):
            rh_mesh.Normals.SetNormal(i, normal[0], normal[1], normal[2])

    # colors
    if len(df_mesh.colors_vertex) > 0:
        for i, color in enumerate(df_mesh.colors_vertex):
            rh_mesh.VertexColors.SetColor(i, color[0], color[1], color[2])

    return rh_mesh

def cvt_rhmesh_2_dfmesh(rh_mesh: rg.Mesh) -> diffcheck_bindings.dfb_geometry.DFMesh:
    """
        Convert a Rhino mesh to a diffCheck mesh.

        :param rh_mesh: rhino mesh

        :return df_mesh: diffCheck mesh
    """
    if not isinstance(rh_mesh, rg.Mesh):
        raise ValueError("rh_mesh should be a Mesh")

    df_mesh = diffcheck_bindings.dfb_geometry.DFMesh()

    if rh_mesh.Vertices.Count == 0:
        print("The input rhino mesh is empty")
        return df_mesh

    # vertices
    rh_vertices = rh_mesh.Vertices.ToFloatArray()
    vertices = []
    for i in range(0, len(rh_vertices), 3):
        vertices.append([rh_vertices[i], rh_vertices[i + 1], rh_vertices[i + 2]])
    df_mesh.vertices = vertices

    # faces
    rh_faces = rh_mesh.Faces
    faces = []
    for i in range(len(rh_faces)):
        face = rh_faces[i]
        faces.append([face.A, face.B, face.C])
    df_mesh.faces = faces

    # normals
    if rh_mesh.Normals.Count > 0:
        normals = rh_mesh.Normals.ToFloatArray()
        normals_vertex = []
        for i in range(0, len(normals), 3):
            normals_vertex.append([normals[i], normals[i + 1], normals[i + 2]])
        df_mesh.normals_vertex = normals_vertex

    # colors
    if rh_mesh.VertexColors.Count > 0:
        colors = rh_mesh.VertexColors.ToArgbColors()
        colors_vertex = []
        for i in range(len(colors)):
            color = colors[i]
            colors_vertex.append([color.R, color.G, color.B])
        df_mesh.colors_vertex = colors_vertex

    return df_mesh

def cvt_dfxform_2_rhxform(df_xform : diffcheck_bindings.dfb_transformation.DFTransformation) -> rg.Transform:
    """
        Convert a diffCheck transformation to a Rhino transformation.

        :param df_xform: diffCheck transformation
        :return rh_xform: rhino transformation
    """
    if not isinstance(df_xform, diffcheck_bindings.dfb_transformation.DFTransformation):
        raise ValueError("df_xform should be a DFTransformation")

    rh_xform = rg.Transform()

    # translation
    translation = df_xform.translation_vector
    rh_xform = rg.Transform.Translation(translation[0], translation[1], translation[2])

    # rotation
    rotation = df_xform.rotation_matrix
    rh_xform = rh_xform * rg.Transform.Rotation(rotation[0], rg.Vector3d(rotation[1], rotation[2], rotation[3]), rg.Point3d(0, 0, 0))

    return rh_xform
def cvt_dfOBB_2_rhbrep(df_OBB) -> rg.Box:
    """ Convert a diffCheck OBB to a Rhino Brep.

        :param df_OBB: diffCheck OBB

        :return rh_obb_brep: the brep box object
    """
    rh_pts = []
    for pt in df_OBB:
        rh_pts.append(rg.Point3d(pt[0], pt[1], pt[2]))

    surfaces = []
    surfaces.append(rg.NurbsSurface.CreateFromCorners(rh_pts[0], rh_pts[1], rh_pts[7], rh_pts[2]))
    surfaces.append(rg.NurbsSurface.CreateFromCorners(rh_pts[0], rh_pts[1], rh_pts[6], rh_pts[3]))
    surfaces.append(rg.NurbsSurface.CreateFromCorners(rh_pts[3], rh_pts[6], rh_pts[4], rh_pts[5]))
    surfaces.append(rg.NurbsSurface.CreateFromCorners(rh_pts[2], rh_pts[7], rh_pts[4], rh_pts[5]))
    surfaces.append(rg.NurbsSurface.CreateFromCorners(rh_pts[1], rh_pts[6], rh_pts[4], rh_pts[7]))
    surfaces.append(rg.NurbsSurface.CreateFromCorners(rh_pts[0], rh_pts[3], rh_pts[5], rh_pts[2]))

    rh_obb_brep = rg.Brep.JoinBreps([rg.Brep.CreateFromSurface(srf) for srf in surfaces], sc.doc.ModelAbsoluteTolerance)[0]

    if rh_obb_brep is None:
        raise ValueError("The OBB could not be converted to a Rhino Brep")
    if not rh_obb_brep.IsValid:
        raise ValueError("The OBB Rhino Brep is not valid")
    if not rh_obb_brep.IsSolid:
        raise ValueError("The OBB Rhino Brep is not solid")

    return rh_obb_brep
