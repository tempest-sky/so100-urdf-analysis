"""
逆运动学（Inverse Kinematics）求解器
使用数值法（雅可比伪逆）求解 SO-ARM100 机械臂的逆运动学问题
"""

import numpy as np
from yourdfpy import URDF

# 加载 URDF
urdf_path = r"C:\Users\asus\so100_urdf\so100_with_marker.urdf"
robot = URDF.load(urdf_path)

joint_names = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
base_link = "base"
end_link = "gripper"


def compute_fk_position(angles):
    """计算正向运动学，返回末端相对于基座的变换矩阵"""
    cfg = dict(zip(joint_names, angles))
    robot.update_cfg(cfg)
    return robot.get_transform(base_link, end_link)


def compute_numerical_jacobian(angles, delta=1e-5):
    """通过数值扰动计算雅可比矩阵 (3x6)"""
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


def solve_ik(target_pos, initial_angles=None, max_iter=100, tolerance=1e-4, damping=0.5):
    """
    数值法逆运动学求解
    参数:
        target_pos: 目标位置 [x, y, z]
        initial_angles: 初始关节角度
        max_iter: 最大迭代次数
        tolerance: 位置误差容限
        damping: 阻尼系数（防止奇异）
    """
    if initial_angles is None:
        angles = np.zeros(6)
    else:
        angles = np.array(initial_angles, dtype=float)

    for i in range(max_iter):
        T_current = compute_fk_position(angles)
        pos_current = T_current[:3, 3]
        
        error = target_pos - pos_current
        error_norm = np.linalg.norm(error)
        
        if error_norm < tolerance:
            print(f"迭代收敛！迭代次数: {i+1}, 误差: {error_norm:.6f} m")
            break
        
        J = compute_numerical_jacobian(angles)
        J_T = J.T
        JJ_T = J @ J_T + damping * np.eye(3)
        J_pseudo = J_T @ np.linalg.inv(JJ_T)
        
        delta_angles = J_pseudo @ error
        angles = angles + delta_angles
    
    return angles, error_norm


def check_joint_limits(angles):
    """检查关节角度是否在限位范围内"""
    limits = {
        "shoulder_pan": (-2.0, 2.0),
        "shoulder_lift": (0, 3.5),
        "elbow_flex": (-np.pi, 0),
        "wrist_flex": (-2.5, 1.2),
        "wrist_roll": (-np.pi, np.pi),
        "gripper": (-0.2, 2.0),
    }
    
    for name, angle in zip(joint_names, angles):
        lower, upper = limits[name]
        status = "OK" if lower <= angle <= upper else "超出限位"
        print(f"  {name}: {angle:.4f} rad [{lower:.2f}, {upper:.2f}] -> {status}")


if __name__ == "__main__":
    print("=" * 50)
    print("SO-ARM100 逆运动学求解器")
    print("=" * 50)
    
    test_cases = [
        [0.2, 0.0, 0.2],
        [0.15, 0.1, 0.15],
        [0.1, 0.0, 0.1],
    ]
    
    for i, target in enumerate(test_cases, 1):
        target_pos = np.array(target)
        print(f"\n测试 {i}: 目标位置 = ({target_pos[0]:.2f}, {target_pos[1]:.2f}, {target_pos[2]:.2f})")
        print("-" * 40)
        
        solved_angles, error = solve_ik(target_pos, max_iter=100, tolerance=1e-4)
        
        print(f"\n求解结果:")
        print(f"  目标位置: ({target_pos[0]:.4f}, {target_pos[1]:.4f}, {target_pos[2]:.4f})")
        
        T_result = compute_fk_position(solved_angles)
        actual_pos = T_result[:3, 3]
        print(f"  实际位置: ({actual_pos[0]:.4f}, {actual_pos[1]:.4f}, {actual_pos[2]:.4f})")
        print(f"  位置误差: {error:.6f} m")
        
        print(f"\n关节角度:")
        for name, angle in zip(joint_names, solved_angles):
            print(f"  {name}: {angle:.4f} rad ({np.degrees(angle):.2f}°)")
        
        print(f"\n限位检查:")
        check_joint_limits(solved_angles)
