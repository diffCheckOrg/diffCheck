from scriptcontext import sticky as rh_sticky_dict
import json
from dataclasses import dataclass, field

@dataclass
class DFPose:
    """
    This class represents the pose of a single element at a given time in the assembly process.
    """
    origin: list
    xDirection: list
    yDirection: list

@dataclass
class DFPosesBeam:
    """
    This class contains the poses of a single beam, at different times in the assembly process.
    It also contains the number of faces detected for this element, based on which the poses are calculated.
    """
    poses_dictionnary: dict
    n_faces: int = 3

    def add_pose(self, pose: DFPose, step_number: int):
        """
        Add a pose to the dictionary of poses.
        """
        self.poses_dictionnary[f"pose_{step_number}"] = pose

    def set_n_faces(self, n_faces: int):
        """
        Set the number of faces detected for this element.
        """
        self.n_faces = n_faces

@dataclass
class DFPosesAssembly:
    n_step: int = 0
    poses_per_element_dictionary: dict = field(default_factory=lambda: rh_sticky_dict)

    """
    This class contains the poses of the different elements of the assembly, at different times in the assembly process.
    """
    def __post_init__(self):
        """
        Initialize the poses_per_element_dictionary with empty DFPosesBeam objects.
        """
        lengths = []
        for element in self.poses_per_element_dictionary:
            lengths.append(len(self.poses_per_element_dictionary[element].poses_dictionnary))
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
            last_poses.append(self.poses_per_element_dictionary[f"element_{i}"].poses_dictionnary[f"pose_{self.n_step-1}"])
        return last_poses

    def reset(self):
        """
        Reset the assembly poses to the initial state.
        """
        self.n_step = 0
        rh_sticky_dict.clear()

    def save(self, file_path: str):
        """
        Save the assembly poses to a JSON file.
        """
        with open(file_path, 'w') as f:
            json.dump(self.poses_per_element_dictionary, f, default=lambda o: o.__dict__, indent=4)


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
        sorted_vectors_by_alignment = sorted(vectors, key=lambda v: compute_dot_product(v, previous_xDirection), reverse=True)
        new_xDirection = sorted_vectors_by_alignment[0]
    else:
        new_xDirection = vectors[0]

    condidates_for_yDirection = []
    for v in vectors:
        if compute_dot_product(v, new_xDirection) ** 2 < 0.5:
            condidates_for_yDirection.append(v)
    if previous_xDirection is not None and previous_yDirection is not None:
        sorted_vectors_by_perpendicularity = sorted(condidates_for_yDirection, key=lambda v: compute_dot_product(v, previous_yDirection), reverse=True)
        new_xDirection = sorted_vectors_by_alignment[0]
        new_yDirection = sorted_vectors_by_perpendicularity[0] - compute_dot_product(sorted_vectors_by_perpendicularity[0], new_xDirection) * new_xDirection
        new_yDirection.Unitize()
    else:
        new_xDirection = vectors[0]
        sorted_vectors = sorted(vectors[1:], key=lambda v: compute_dot_product(v, new_xDirection)**2)
        new_yDirection = sorted_vectors[0] - compute_dot_product(vectors[1], new_xDirection) * new_xDirection
        new_yDirection.Unitize()
    return new_xDirection, new_yDirection
