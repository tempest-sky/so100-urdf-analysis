"""
轨迹规划（Trajectory Planning）
实现机械臂末端直线轨迹规划与可视化
"""

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


def linear_trajectory(start_pos, end_pos, num_steps=50):
    t = np.linspace(0, 1, num_steps)
    trajectory = []
    for ti in t:
        pos = (1 - ti) * np.array(start_pos) + ti * np.array(end_pos)
        trajectory.append(pos)
    return trajectory


def plan_and_execute(start_pos, end_pos, num_steps=50, init_angles=None):
    if init_angles is None:
        init_angles = np.zeros(6)
    
    trajectory = linear_trajectory(start_pos, end_pos, num_steps)
    
    print(f"轨迹规划: 起点 ({start_pos[0]:.3f}, {start_pos[1]:.3f}, {start_pos[2]:.3f})")
    print(f"         终点 ({end_pos[0]:.3f}, {end_pos[1]:.3f}, {end_pos[2]:.3f})")
    print(f"         步数: {num_steps}")
    print("-" * 50)
    
    joint_trajectory = []
    actual_positions = []
    
    current_angles = init_angles
    for i, target_pos in enumerate(trajectory):
        angles = solve_ik_step(target_pos, current_angles)
        angles = clamp_joint_limits(angles)
        
        T_actual = compute_fk_position(angles)
        actual_pos = T_actual[:3, 3]
        
        joint_trajectory.append(angles)
        actual_positions.append(actual_pos)
        current_angles = angles
    
    print("规划完成！")
    return joint_trajectory, actual_positions


def visualize_trajectory_3d(actual_positions, start_pos, end_pos):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    actual_positions = np.array(actual_positions)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(actual_positions[:, 0], actual_positions[:, 1], actual_positions[:, 2],
            'b-', linewidth=2, label='实际轨迹')
    ax.scatter([start_pos[0]], [start_pos[1]], [start_pos[2]],
               c='green', s=100, marker='o', label='起点')
    ax.scatter([end_pos[0]], [end_pos[1]], [end_pos[2]],
               c='red', s=100, marker='x', label='终点')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('末端直线轨迹规划')
    ax.legend()
    ax.set_box_aspect([1, 1, 1])
    
    plt.tight_layout()
    plt.savefig('trajectory_result.png', dpi=150, bbox_inches='tight')
    print("\n轨迹图已保存为: trajectory_result.png")
    plt.show()


if __name__ == "__main__":
    print("=" * 50)
    print("SO-ARM100 直线轨迹规划")
    print("=" * 50)
    
    start = [0.15, 0.0, 0.15]
    end = [0.25, 0.1, 0.25]
    
    joint_traj, actual_pos = plan_and_execute(start, end, num_steps=50)
    
    print(f"\n最终关节角度:")
    final_angles = joint_traj[-1]
    for name, angle in zip(joint_names, final_angles):
        print(f"  {name}: {angle:.4f} rad ({np.degrees(angle):.2f}°)")
    
    visualize_trajectory_3d(actual_pos, start, end)
