#! python3
"""
    This module contains the utility functions to compute the difference between source and target
"""

import numpy as np


def cloud_2_cloud_distance(source, target, signed=False):
    """
        Compute the Euclidean distance for every point of a source pcd to its closest point on a target pointcloud
    """
    distances = np.full(len(source.points), np.inf)

    for i in range(len(source.points)):

        dists = np.linalg.norm(np.asarray(target.points) - np.asarray(source.points)[i], axis=1)
        distances[i] = np.min(dists)

        # determine whether the point on the source cloud is in the same direction as the normal of the corresponding point on the target pcd
        if signed:
            closest_idx = np.argmin(dists)
            # direction from target to source
            direction = source.points[i] - target.points[closest_idx]
            distances[i] *= np.sign(np.dot(direction, target.normals[closest_idx]))

    return distances


def cloud_2_mesh_distance(source, target):
    """
        Calculate the distance between every point of a source pcd to its closest point on a target mesh
    """

    # for every point on the PCD compute the point_2_mesh_distance

    distances = np.ones(len(source.points), dtype=float)

    return distances


def point_2_mesh_distance(mesh, point):
     """
        Calculate the closest distance between a point and a mesh
    """
    pass
    # make a kdtree of the vertices to get the relevant vertices indexes
    pcd = o3d.geometry.PointCloud()
    pcd.points = mesh.vertices
    kd_tree = o3d.geometry.KDTreeFlann(pcd)

    # assume smallest distance is the distance to the closest vertex
    [_, idx, _] = kd_tree.search_knn_vector_3d(query_point, 1)
    if idx>=0:
        nearest_vertex_idx = idx[0]
    else:
        raise ValueError("The mesh has no vertices. Please provide a mesh.")
    nearest_vertex = np.asarray(mesh.vertices)[nearest_vertex_idx]
    dist = np.linalg.norm(query_point - nearest_vertex)

    
    # create a box centered around the query point with an edge length equal to two times the distance to the nearest vertex
    search_distance = dist * 2
        if dist > search_distance:
            return dist

    search_box_min = query_point - search_distance
    search_box_max = query_point + search_distance

    def face_in_box(face):
        v0, v1, v2 = face
        vertices = np.asarray(mesh.vertices)
        return (np.all(vertices[v0] >= search_box_min) and np.all(vertices[v0] <= search_box_max) or
                np.all(vertices[v1] >= search_box_min) and np.all(vertices[v1] <= search_box_max) or
                np.all(vertices[v2] >= search_box_min) and np.all(vertices[v2] <= search_box_max))
    
    candidate_faces = [face for face in np.asarray(mesh.triangles) if face_in_box(face)]
    

    # query a kd tree for all the faces that intersect this box

    # compute the closest point for the faces that we get back
        
    
def point_2_face_distance(face,  point):
    """
        Calculate the closest distance between a point and a face
    """

    if len(face.vertices) == 3:
        return point_2_triangle_distance(point, face)
    elif len(face.vertices) == 4:
        return point_2_quad_distance(point, face)
    else:
        raise ValueError("Face must be a triangle or quadrilateral")


def point_2_triangle_distance(point, triangle):
    """
        Calculate the shortest distance from a point to a triangle.
    """
    a, b, c = triangle

    bary_coords = barycentric_coordinates(point, a, b, c)

    # If the point is inside or on the triangle, use the barycentric coordinates to find the closest point
    if np.all(bary_coords >= 0):
        closest_point = bary_coords[0] * a + bary_coords[1] * b + bary_coords[2] * c
    
    # If the point is outside the triangle, project it onto the triangle edges and find the closest point
    else:
        proj = np.array([np.dot(point - a, b - a) / np.dot(b - a, b - a), 
                         np.dot(point - b, c - b) / np.dot(c - b, c - b), 
                         np.dot(point - c, a - c) / np.dot(a - c, a - c)])
        proj = np.clip(proj, 0, 1)
        closest_point = np.array([a + proj[0] * (b - a), b + proj[1] * (c - b), c + proj[2] * (a - c)]).min(axis=0)
    
    return np.linalg.norm(closest_point - point)


def barycentric_coordinates(p, a, b, c):
    """
        Calculate the barycentric coordinates of point p with respect to the triangle defined by points a, b, and c.
    """
    v0 = b - a
    v1 = c - a
    v2 = p - a

    d00 = np.dot(v0, v0)
    d01 = np.dot(v0, v1)
    d11 = np.dot(v1, v1)
    d20 = np.dot(v2, v0)
    d21 = np.dot(v2, v1)

    denom = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    return np.array([u, v, w])


def point_2_quad_distance(point, quad):
    """
        Calculate the shortest distance from a point to a quadrilateral.
    """
    a, b, c, d = quad.vertices
    
    # Calculate the distance to the two triangles that form the quadrilateral
    return min(point_2_triangle_distance(point, [a, b, c]), 
               point_2_triangle_distance(point, [c, d, a]))


def compute_mse(distances):
    """
        Calculate mean squared distance
    """
    mse = np.sqrt(np.mean(distances ** 2))

    return mse


def compute_max_deviation(distances):
    """
        Calculate max deviation of distances
    """
    max_deviation = np.max(distances)

    return max_deviation


def compute_min_deviation(distances):
    """
        Calculate min deviation of distances
    """

    min_deviation = np.min(distances)

    return min_deviation


def compute_standard_deviation(distances):
    """
        Calculate standard deviation of distances
    """
    standard_deviation = np.std(distances)

    return standard_deviation
