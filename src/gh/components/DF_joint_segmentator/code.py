import Rhino
import diffCheck
from diffCheck import diffcheck_bindings
from diffCheck import df_cvt_bindings as df_cvt
import diffCheck.df_util

def main():
    # assume two inputs: i_cloud and i_joints. i_cloud is the point cloud of the whole object, i_joints is a list of list the meshes of the joints. [[face_1_joint_A, face_2_joint_A, ...], [face_1_joint_B, face_2_joint_B, ...], ...]
    # segment the joints from the i_cloud and store them in a list that follows the same structure as i_joints: [joint_A, joint_B, ...]
    # for each joint point cloud, perform a registration by populating the corresponding mesh faces of each joint
    # apply the registration to the segmented joint point cloud and re-segment the joints
    # the result is a list of list of the segmented joints, where each segment is locally registered to the corresponding mesh faces: [[face_1_joint_A_arfter_reg_a, face_2_joint_A_after_reg_a, ...], [face_1_joint_B_after_reg_b, face_2_joint_B_after_reg_b, ...], ...]
    # that way we can analyse the joints individually (face 1 of joint A is too much to the left, ...)
    pass

if __name__ == "__main__":
    a = main()