"""Compares CAD poses with measured poses to compute errors."""
#! python3

import Rhino
import Grasshopper
from ghpythonlib.componentbase import executingcomponent as component
import ghpythonlib.treehelpers as th

import diffCheck.df_geometries
import numpy

def compute_comparison(measured_pose, cad_pose):
    cad_origin = cad_pose.Origin
    measured_origin = measured_pose.Origin
    distance = cad_origin.DistanceTo(measured_origin)

    # Compare the orientations using the formula: $$ \theta = \arccos\left(\frac{\text{trace}(R_{\text{pred}}^T R_{\text{meas}}) - 1}{2}\right) $$
    transform_o_to_cad = Rhino.Geometry.Transform.PlaneToPlane(Rhino.Geometry.Plane.WorldXY, cad_pose)
    transform_o_to_measured = Rhino.Geometry.Transform.PlaneToPlane(Rhino.Geometry.Plane.WorldXY, measured_pose)
    np_transform_o_to_cad = numpy.array(transform_o_to_cad.ToDoubleArray(rowDominant=True)).reshape((4, 4))
    np_transform_o_to_measured = numpy.array(transform_o_to_measured.ToDoubleArray(rowDominant=True)).reshape((4, 4))

    R_cad = np_transform_o_to_cad[:3, :3]
    R_measured = np_transform_o_to_measured[:3, :3]
    R_rel = numpy.dot(R_cad.T, R_measured)
    theta = numpy.arccos(numpy.clip((numpy.trace(R_rel) - 1) / 2, -1.0, 1.0))

    # Compute the transformation matrix between the CAD pose and the measured pose
    transform_cad_to_measured = Rhino.Geometry.Transform.PlaneToPlane(cad_pose, measured_pose)
    return distance, theta, transform_cad_to_measured

class DFPoseComparison(component):
    def RunScript(self, i_assembly: diffCheck.df_geometries.DFAssembly, i_measured_planes: Grasshopper.DataTree[object]):

        CAD_poses = [beam.plane for beam in i_assembly.beams]

        o_distances = []
        o_angles = []
        o_transforms_cad_to_measured = []
        # Compare the origins
        #   measure the distance between the origins of the CAD pose and the measured pose and output this in the component

        bc = i_measured_planes.BranchCount
        if bc > 1:
            poses_per_beam = i_measured_planes.Branches
            for beam_id, poses in enumerate(poses_per_beam):
                o_distances.append(bc * [])
                o_angles.append(bc * [])
                o_transforms_cad_to_measured.append(bc * [])
                for pose in poses:
                    if not pose:
                        o_distances[beam_id].append(None)
                        o_angles[beam_id].append(None)
                        o_transforms_cad_to_measured[beam_id].append(None)
                    else:
                        dist, angle, transform_cad_to_measured = compute_comparison(pose, CAD_poses[beam_id])
                        o_distances[beam_id].append(dist)
                        o_angles[beam_id].append(angle)
                        o_transforms_cad_to_measured[beam_id].append(transform_cad_to_measured)
        else:
            i_measured_planes.Flatten()
            measured_plane_list = th.tree_to_list(i_measured_planes)
            print(measured_plane_list)
            for i, plane in enumerate(measured_plane_list):
                dist, angle, transform_cad_to_measured = compute_comparison(plane, CAD_poses[i])
                o_distances.append(dist)
                o_angles.append(angle)
                o_transforms_cad_to_measured.append(transform_cad_to_measured)

        if bc == 1:
            return o_distances, o_angles, o_transforms_cad_to_measured
        else:
            return th.list_to_tree(o_distances), th.list_to_tree(o_angles), th.list_to_tree(o_transforms_cad_to_measured)
