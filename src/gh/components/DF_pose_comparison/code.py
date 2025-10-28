#! python3

import Rhino
from ghpythonlib.componentbase import executingcomponent as component

import System

import diffCheck.df_geometries
import numpy


class DFPoseComparison(component):
    def RunScript(self,
            i_assembly: diffCheck.df_geometries.DFAssembly,
            i_measured_poses: System.Collections.Generic.List[Rhino.Geometry.Plane]):

        CAD_poses = [beam.plane for beam in i_assembly.beams]

        o_distances = []
        o_angles = []
        o_transforms_cad_to_measured = []
        # Compare the origins
        #   measure the distance between the origins of the CAD pose and the measured pose and output this in the component
        for i in range(len(i_measured_poses)):
            cad_origin = CAD_poses[i].Origin
            measured_origin = i_measured_poses[i].Origin
            distance = cad_origin.DistanceTo(measured_origin)
            o_distances.append(distance)

            # Compare the orientations using the formula: $$ \theta = \arccos\left(\frac{\text{trace}(R_{\text{pred}}^T R_{\text{meas}}) - 1}{2}\right) $$
            transform_o_to_cad = Rhino.Geometry.Transform.PlaneToPlane(Rhino.Geometry.Plane.WorldXY, CAD_poses[i])
            transform_o_to_measured = Rhino.Geometry.Transform.PlaneToPlane(Rhino.Geometry.Plane.WorldXY, i_measured_poses[i])
            np_transform_o_to_cad = numpy.array(transform_o_to_cad.ToDoubleArray(rowDominant=True)).reshape((4, 4))
            np_transform_o_to_measured = numpy.array(transform_o_to_measured.ToDoubleArray(rowDominant=True)).reshape((4, 4))

            R_cad = np_transform_o_to_cad[:3, :3]
            R_measured = np_transform_o_to_measured[:3, :3]
            R_rel = numpy.dot(R_cad.T, R_measured)
            theta = numpy.arccos(numpy.clip((numpy.trace(R_rel) - 1) / 2, -1.0, 1.0))
            o_angles.append(theta)

            # Compute the transformation matrix between the CAD pose and the measured pose
            transform_cad_to_measured = Rhino.Geometry.Transform.PlaneToPlane(CAD_poses[i], i_measured_poses[i])
            o_transforms_cad_to_measured.append(transform_cad_to_measured)

        return [o_distances, o_angles, o_transforms_cad_to_measured]
