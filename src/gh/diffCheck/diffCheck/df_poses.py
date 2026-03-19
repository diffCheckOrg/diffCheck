from scriptcontext import sticky as rh_sticky_dict
import ghpythonlib.treehelpers as th
import Rhino

import json
import numpy
from dataclasses import dataclass, field

# use a key and not all the sticky
_STICKY_KEY = "df_poses"

def _get_store():
    # returns private sub-dict inside rhino sticky
    return rh_sticky_dict.setdefault(_STICKY_KEY, {})

@dataclass
class DFPose:
    """
    This class represents the pose of a single element at a given time in the assembly process.
    """
    origin: list
    xDirection: list
    yDirection: list

    def to_rh_plane(self):
        """
        Convert the pose to a Rhino Plane object.
        """
        origin = Rhino.Geometry.Point3d(self.origin[0], self.origin[1], self.origin[2])
        xDirection = Rhino.Geometry.Vector3d(self.xDirection[0], self.xDirection[1], self.xDirection[2])
        yDirection = Rhino.Geometry.Vector3d(self.yDirection[0], self.yDirection[1], self.yDirection[2])
        return Rhino.Geometry.Plane(origin, xDirection, yDirection)

    def compare_to_rh_plane(self, rh_plane):
        """
        Compare this pose to another pose and return the differences in origin, xDirection and yDirection.

        :param rh_plane: the Rhino Plane to compare to
        :return: a tuple containing the distance between the origins, the angle between the xDirections and the rhino transform to go from the compared pose to this pose.
        """
        other_origin = rh_plane.Origin
        measured_origin = self.to_rh_plane().Origin
        distance = other_origin.DistanceTo(measured_origin)

        # Compare the orientations using the formula: $$ \theta = \arccos\left(\frac{\text{trace}(R_{\text{pred}}^T R_{\text{meas}}) - 1}{2}\right) $$
        transform_o_to_other = Rhino.Geometry.Transform.PlaneToPlane(Rhino.Geometry.Plane.WorldXY, rh_plane)
        transform_o_to_current = Rhino.Geometry.Transform.PlaneToPlane(Rhino.Geometry.Plane.WorldXY, self.to_rh_plane())
        np_transform_o_to_other = numpy.array(transform_o_to_other.ToDoubleArray(rowDominant=True)).reshape((4, 4))
        np_transform_o_to_measured = numpy.array(transform_o_to_current.ToDoubleArray(rowDominant=True)).reshape((4, 4))

        R_other = np_transform_o_to_other[:3, :3]
        R_measured = np_transform_o_to_measured[:3, :3]
        R_rel = numpy.dot(R_other.T, R_measured)
        theta = numpy.arccos(numpy.clip((numpy.trace(R_rel) - 1) / 2, -1.0, 1.0))

        transform_other_to_current_plane = Rhino.Geometry.Transform.PlaneToPlane(rh_plane, self.to_rh_plane())
        return distance, theta, transform_other_to_current_plane

@dataclass
class DFPosesBeam:
    """
    This class contains the poses of a single beam, at different times in the assembly process.
    It also contains the number of faces detected for this element, based on which the poses are calculated.
    """
    poses_dictionary: dict
    n_faces: int = 3

    def add_pose(self, pose: DFPose, step_number: int):
        """
        Add a pose to the dictionary of poses.
        """
        self.poses_dictionary[f"pose_{step_number}"] = pose

    def set_n_faces(self, n_faces: int):
        """
        Set the number of faces detected for this element.
        """
        self.n_faces = n_faces

@dataclass
class DFPosesAssembly:
    n_step: int = 0
    poses_per_element_dictionary: dict = field(default_factory=_get_store)

    """
    This class contains the poses of the different elements of the assembly, at different times in the assembly process.
    """
    def __post_init__(self):
        """
        Initialize the poses_per_element_dictionary with empty DFPosesBeam objects.
        """
        lengths = []
        for element in self.poses_per_element_dictionary:
            lengths.append(len(self.poses_per_element_dictionary[element].poses_dictionary))
        self.n_step = max(lengths) if lengths else 0

    def add_step(self, new_poses: list[DFPose]):
        for i, pose in enumerate(new_poses):
            if f"element_{i}" not in self.poses_per_element_dictionary:
                self.poses_per_element_dictionary[f"element_{i}"] = DFPosesBeam({}, 4)
                for j in range(self.n_step):
                    self.poses_per_element_dictionary[f"element_{i}"].add_pose(None, j)
            self.poses_per_element_dictionary[f"element_{i}"].add_pose(pose, self.n_step)
        self.n_step += 1

    def get_last_poses(self):
        """
        Get the last poses of each element.
        """
        if self.n_step == 0:
            return None
        last_poses = []
        for i in range(len(self.poses_per_element_dictionary)):
            last_poses.append(self.poses_per_element_dictionary[f"element_{i}"].poses_dictionary[f"pose_{self.n_step-1}"])
        return last_poses

    def reset(self):
        """
        Reset the assembly poses to the initial state.
        """
        self.n_step = 0
        # clear only namespace
        rh_sticky_dict[_STICKY_KEY] = {}
        # refresh the local reference to the (now empty) store
        self.poses_per_element_dictionary = _get_store()

    def save(self, file_path: str):
        """
        Save the assembly poses to a JSON file.
        """
        with open(file_path, 'w') as f:
            json.dump(self.poses_per_element_dictionary, f, default=lambda o: o.__dict__, indent=4)

    def to_gh_tree(self):
        """
        Convert the assembly poses to a Grasshopper tree structure.
        """
        list_of_poses = []
        for element, poses in self.poses_per_element_dictionary.items():
            list_of_pose_of_element = []
            for pose in poses.poses_dictionary.values():
                list_of_pose_of_element.append(pose.to_rh_plane() if pose is not None else None)
            list_of_poses.append(list_of_pose_of_element)
        return th.list_to_tree(list_of_poses)

    def from_gh_tree(self, gh_tree):
        """
        Load the assembly poses from a Grasshopper tree structure.

        :param gh_tree: the Grasshopper tree containing the poses in the form of Rhino Planes
        """
        bc = gh_tree.BranchCount
        if bc > 1:
            list_of_poses = th.tree_to_list(gh_tree)
        else:
            gh_tree.Flatten()
            list_of_poses = [th.tree_to_list(gh_tree)]
        n_poses = len(list_of_poses[0]) if list_of_poses else 0
        for i in range(n_poses):
            new_poses = []
            for poses_of_element in list_of_poses:
                if poses_of_element[i] is None:
                    new_poses.append(None)
                    continue
                new_poses.append(DFPose(
                    origin = [poses_of_element[i].Origin.X, poses_of_element[i].Origin.Y, poses_of_element[i].Origin.Z],
                    xDirection = [poses_of_element[i].XAxis.X, poses_of_element[i].XAxis.Y, poses_of_element[i].XAxis.Z],
                    yDirection = [poses_of_element[i].YAxis.X, poses_of_element[i].YAxis.Y, poses_of_element[i].YAxis.Z]))
            self.add_step(new_poses)


def compute_dot_product(v1, v2):
    """
    Compute the dot product of two vectors.
    """
    return (v1.X * v2.X) + (v1.Y * v2.Y) + (v1.Z * v2.Z)


def select_vectors(vectors, previous_xDirection, previous_yDirection):
    """
    Select the vectors that are aligned with the xDirection and yDirection.
    """
    if previous_xDirection is not None and previous_yDirection is not None:
        sorted_vectors_by_alignment = sorted(vectors, key=lambda v: abs(compute_dot_product(v, previous_xDirection)), reverse=True)
        new_xDirection = sorted_vectors_by_alignment[0]
    else:
        new_xDirection = vectors[0]
    new_xDirection.Unitize()

    if previous_xDirection is not None and previous_yDirection is not None:
        sorted_vectors_by_perpendicularity = sorted(vectors, key=lambda v: abs(compute_dot_product(v, previous_xDirection)))
        new_yDirection = sorted_vectors_by_perpendicularity[0] - compute_dot_product(sorted_vectors_by_perpendicularity[0], new_xDirection) * new_xDirection
        if compute_dot_product(new_xDirection, previous_xDirection) < 0:
            new_xDirection = -sorted_vectors_by_alignment[0]
        if compute_dot_product(new_yDirection, previous_yDirection) < 0:
            new_yDirection = -new_yDirection
        new_yDirection.Unitize()
    else:
        sorted_vectors = sorted(vectors[1:], key=lambda v: abs(compute_dot_product(v, new_xDirection)))
        new_yDirection = sorted_vectors[0] - compute_dot_product(sorted_vectors[0], new_xDirection) * new_xDirection
        if previous_yDirection is not None and compute_dot_product(new_yDirection, previous_yDirection) < 0:
            new_yDirection = -new_yDirection
        new_yDirection.Unitize()

    return new_xDirection, new_yDirection
