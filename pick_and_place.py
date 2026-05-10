"""
Pick & Place 仿真任务
在 Rerun Viewer 中可视化机械臂抓取和放置物体的过程
"""

import rerun as rr
import numpy as np
import time

from yourdfpy import URDF

urdf_path = r"C:\Users\asus\so100_urdf\so100_with_marker.urdf"
robot = URDF.load(urdf_path)

joint_names = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
base_link = "base"
end_link = "gripper"

joint_limits = {
    "shoulder_pan": (-2.0, 2.0),
    "shoulder_lift": (0, 3.5),
    "elbow_flex": (-np.pi, 0),
    "wrist_flex": (-2.5, 1.2),
    "wrist_roll": (-np.pi, np.pi),
    "gripper": (-0.2, 2.0),
}


def compute_fk_position(angles):
    cfg = dict(zip(joint_names, angles))
    robot.update_cfg(cfg)
    return robot.get_transform(base_link, end_link)


def compute_numerical_jacobian(angles, delta=1e-5):
    n_joints = len(angles)
    T_base = compute_fk_position(angles)
    pos_base = T_base[:3, 3]
    J = np.zeros((3, n_joints))
    for i in range(n_joints):
        angles_perturbed = angles.copy()
        angles_perturbed[i] += delta
        T_perturbed = compute_fk_position(angles_perturbed)
        pos_perturbed = T_perturbed[:3, 3]
        J[:, i] = (pos_perturbed - pos_base) / delta
    return J


def solve_ik_step(target_pos, angles, max_iter=50, damping=0.5):
    for _ in range(max_iter):
        T_current = compute_fk_position(angles)
        pos_current = T_current[:3, 3]
        error = target_pos - pos_current
        if np.linalg.norm(error) < 1e-4:
            break
        J = compute_numerical_jacobian(angles)
        J_T = J.T
        JJ_T = J @ J_T + damping * np.eye(3)
        J_pseudo = J_T @ np.linalg.inv(JJ_T)
        angles = angles + J_pseudo @ error
    return angles


def clamp_joint_limits(angles):
    clamped = angles.copy()
    for i, name in enumerate(joint_names):
        lower, upper = joint_limits[name]
        clamped[i] = np.clip(angles[i], lower, upper)
    return clamped


def move_to_position(target_pos, current_angles, steps=30):
    angles = current_angles.copy()
    joint_traj = []
    for i in range(steps):
        angles = solve_ik_step(target_pos, angles)
        angles = clamp_joint_limits(angles)
        joint_traj.append(angles.copy())
    return joint_traj


def rr_log_robot_state(angles, step_label=""):
    cfg = dict(zip(joint_names, angles))
    robot.update_cfg(cfg)
    for joint in robot.joints:
        if joint.name in cfg:
            transform = joint.compute_transform(cfg[joint.name])
            rr.log(f"transforms/{joint.name}", rr.Transform3D(matrix=transform))


def pick_and_place_demo():
    rr.init("SO-ARM100 Pick & Place", spawn=True)

    urdf_tree = rr.urdf.UrdfTree.from_file_path(urdf_path)
    rr.log_file_from_path(urdf_path, static=True)

    pick_pos = [0.2, 0.0, 0.15]
    above_pick = [0.2, 0.0, 0.22]
    place_pos = [0.15, 0.1, 0.15]
    above_place = [0.15, 0.1, 0.22]

    rr.log("objects/pick_point", rr.Points3D([pick_pos], colors=[[0, 255, 0]], radii=[0.01]))
    rr.log("objects/place_point", rr.Points3D([place_pos], colors=[[255, 0, 0]], radii=[0.01]))

    current_angles = np.zeros(6)

    steps_info = [
        ("1. 移动到抓取点上方", above_pick),
        ("2. 下降到抓取点", pick_pos),
        ("3. 闭合夹爪", pick_pos),
        ("4. 抬起到放置点上方", above_place),
        ("5. 下降到放置点", place_pos),
        ("6. 张开夹爪释放", place_pos),
        ("7. 回到初始位置", above_place),
    ]

    for label, target in steps_info:
        print(f"执行: {label}")
        traj = move_to_position(target, current_angles, steps=20)
        for angles in traj:
            rr_log_robot_state(angles, label)
            current_angles = angles
            time.sleep(0.05)

    print("\nPick & Place 演示完成！")


if __name__ == "__main__":
    pick_and_place_demo()
