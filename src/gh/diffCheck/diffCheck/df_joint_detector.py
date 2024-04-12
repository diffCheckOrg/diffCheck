import Rhino
import scriptcontext as sc
import Rhino.Geometry as rg

import typing
from dataclasses import dataclass

import df_util
import df_transformations
from df_geometries import DFFace

@dataclass
class JointDetector():
    """
    This class is responsible for detecting joints in a brep
    """
    brep : Rhino.Geometry.Brep
    def __post_init__(self):
        self.brep = self.brep or None
        # list of straight cuts
        self._cuts : typing.List[rg.Brep] = []
        # list of holes
        self._holes : typing.List[rg.Brep] = []
        # list of mixed joints (cuts+holes)
        self._mix : typing.List[rg.Brep]= []

        # list of DFFaces from joints and sides
        self._faces : typing.List[DFFace] = []

    def run(self) -> typing.List[DFFace]:
        """
            Run the joint detector

            :return: a list of faces from joins and faces
        """
        ############################################################################
        # 1. Bring to XY, mamke AABB and get negative boolean difference
        ############################################################################
        # bring to plane xy
        x_form = df_transformations.pln_2_pln_world_transform(self.brep)

        # reverse the transformation
        x_form_back = df_transformations.get_inverse_transformation(x_form)

        # compute the bounding box and inflate to include butt joints typo
        bbox = self.brep.GetBoundingBox(True)
        diagonal = bbox.Diagonal
        scaling_factor = diagonal.Length / 10
        bbox.Inflate(scaling_factor, 0, 0)
        bbox_b = bbox.ToBrep()

        # boolean difference between the bounding box and the brep transformed
        breps_from_booldiff = Rhino.Geometry.Brep.CreateBooleanDifference(
            bbox_b, self.brep, sc.doc.ModelAbsoluteTolerance)
        if breps_from_booldiff is None or len(breps_from_booldiff) == 0:
            ghenv.Component.AddRuntimeMessage(RML.Error, "No breps found after boolean difference.")

        ############################################################################
        # 2. Distinguish holes, cuts, and mix boolean difference results
        ############################################################################
        is_hole = False
        is_cut = False
        is_tenon_mortise = False
        is_mix = False

        # parse holes, cuts and mix
        for b in breps_from_booldiff:
            is_cut = True
            for f in b.Faces:
                f_brep = f.ToBrep()
                f = f_brep.Faces[0]
                if not f.IsPlanar():
                    is_cut = False
                    is_hole = True

                    b_faces = df_util.explode_brep(b)
                    for b_face in b_faces:
                        if b_face.Faces[0].IsPlanar():
                            b_face_edges = b_face.Edges
                            for b_face_edge in b_face_edges:
                                if not b_face_edge.IsClosed:
                                    is_mix = True
                                    is_hole = False
                                    break
                            if is_mix:
                                break
                    break

            if is_hole:
                self._holes.append(b)
            elif is_cut: 
                self._cuts.append(b)
            elif is_mix:
                self._mix.append(b)

            is_hole = False
            is_cut = False
            is_mix = False
        
        # deal with mix
        candidate_cuts = []
        candidate_holes = []
        for b in self._mix:
            # -- algorithm draft --
            # (1) explode
            # (2) seperate in tow list flat surfaces (cuts + cylinder's bases) and non flat surfaces (cylinders)
            # (3) cap each object in both lists
            # (4) boolunion every object in both lists
            # (5) check if closed, if it is 
            # ----------------------
            # (1) explode
            faces_b = df_util.explode_brep(b)

            # (2) seperate in tow list flat surfaces (cuts + cylinder's bases) and non flat surfaces (cylinders)
            flat_faces_b = []
            non_flat_faces_b = []
            for f_b in faces_b:
                if f_b.Faces[0].IsPlanar():
                    flat_faces_b.append(f_b)
                else:
                    non_flat_faces_b.append(f_b)
    
            # (*) cap the cylinders
            non_flat_faces_b = [f_b.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance) for f_b in non_flat_faces_b]
            
            # (4) boolunion every object in both lists
            flat_faces_b = Rhino.Geometry.Brep.CreateBooleanUnion(flat_faces_b, sc.doc.ModelAbsoluteTolerance)
            non_flat_faces_b = Rhino.Geometry.Brep.CreateBooleanUnion(non_flat_faces_b, sc.doc.ModelAbsoluteTolerance)

            # (3) cap candidate cuts
            flat_faces_b = [f_b.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance) for f_b in flat_faces_b]
            # non_flat_faces_b = [f_b.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance) for f_b in non_flat_faces_b]

            # (*) merge all coplanar faces in breps cut candidates
            for f_b in flat_faces_b:
                if f_b is not None:
                    f_b.MergeCoplanarFaces(sc.doc.ModelAbsoluteTolerance)

            # (5) check if closed, if it is add to cuts, if not add to holes
            for f_b in flat_faces_b:
                if f_b is not None:
                    if f_b.IsSolid:
                        self._cuts.append(f_b)
            for f_b in non_flat_faces_b:
                if f_b is not None:
                    if f_b.IsSolid:
                        self._holes.append(f_b)

        ############################################################################
        # 3. Sort faces from joints and faces from sides
        ############################################################################
        # retransform back everything
        for b in self._holes:
            b.Transform(x_form_back)
        for b in self._cuts:
            b.Transform(x_form_back)
        for b in self._mix:
            b.Transform(x_form_back)
        self.brep.Transform(x_form_back)

        # get all the medians of the faces of cuts only
        cuts_faces_centroids : typing.Dict[int, typing.List[rg.Point3d]] = {}
        for idx, b in enumerate(self._cuts):
            idx = idx + 1
            temp_face_centroids = []
            for f in b.Faces:
                centroid = DFFace.compute_mass_center(f)
                temp_face_centroids.append(centroid)
            cuts_faces_centroids[idx] = temp_face_centroids

        # compare with the brep medians faces to get the joint/sides's faces
        for f in self.brep.Faces:
            centroid_2test = DFFace.compute_mass_center(f)
            for key, centroids in cuts_faces_centroids.items():
                is_joint = False
                for centroid in centroids:
                    if centroid_2test.DistanceTo(centroid) < sc.doc.ModelAbsoluteTolerance:
                        self._faces.append(DFFace.from_brep(f, key))
                        is_joint = True
                        break
                if is_joint:
                    break
            if not is_joint:
                self._faces.append(DFFace.from_brep(f, None))

        return self._faces