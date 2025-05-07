from scriptcontext import sticky as rh_sticky_dict

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
    """
    poses_dictionnary: dict

    def add_pose(self, pose: DFPose, step_number: int):
        """
        Add a pose to the dictionary of poses.
        """
        self.poses_dictionnary[f"pose_{step_number}"] = pose

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
                self.poses_per_element_dictionary[f"element_{i}"] = DFPosesBeam({})
            self.poses_per_element_dictionary[f"element_{i}"].add_pose(pose, self.n_step + 1)
        self.n_step += 1

    def get_last_poses(self):
        """
        Get the last poses of each element.
        """
        if self.n_step == 0:
            return None
        last_poses = []
        for i in range(len(self.poses_per_element_dictionary)):
            last_poses.append(self.poses_per_element_dictionary[f"element_{i}"].poses_dictionnary[f"pose_{self.n_step}"])
        return last_poses

    def reset(self):
        """
        Reset the assembly poses to the initial state.
        """
        self.n_step = 0
        rh_sticky_dict.clear()
