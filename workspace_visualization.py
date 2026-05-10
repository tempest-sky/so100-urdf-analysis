"""
工作空间（Workspace）可视化
使用蒙特卡洛方法随机采样关节角度，绘制机械臂可达范围
"""

import numpy as np
import matplotlib.pyplot as plt
from yourdfpy import URDF
from mpl_toolkits.mplot3d import Axes3D

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
    "gripper": (-0.2, 0.5),
}

def get_random_joint_angles():
    angles = []
    for name in joint_names:
        lower, upper = joint_limits[name]
        angles.append(np.random.uniform(lower, upper))
    return np.array(angles)


def compute_end_effector_position(angles):
    cfg = dict(zip(joint_names, angles))
    robot.update_cfg(cfg)
    T = robot.get_transform(base_link, end_link)
    return T[:3, 3]


def generate_workspace_points(n_samples=10000):
    points = []
    print(f"开始生成 {n_samples} 个工作空间采样点...")
    for i in range(n_samples):
        angles = get_random_joint_angles()
        pos = compute_end_effector_position(angles)
        points.append(pos)
        if (i + 1) % 2000 == 0:
            print(f"  已完成 {i+1}/{n_samples}")
    return np.array(points)


def plot_workspace(points):
    fig = plt.figure(figsize=(12, 8))

    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(points[:, 0], points[:, 1], points[:, 2],
                s=1, alpha=0.5, c='blue', marker='.')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.set_title('3D 工作空间')
    ax1.set_box_aspect([1, 1, 1])

    ax2 = fig.add_subplot(132)
    ax2.scatter(points[:, 0], points[:, 1], s=1, alpha=0.3, c='red', marker='.')
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_title('XY 平面投影')
    ax2.axis('equal')
    ax2.grid(True, alpha=0.3)

    ax3 = fig.add_subplot(133)
    ax3.scatter(points[:, 0], points[:, 2], s=1, alpha=0.3, c='green', marker='.')
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Z (m)')
    ax3.set_title('XZ 平面投影')
    ax3.axis('equal')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('workspace_visualization.png', dpi=150, bbox_inches='tight')
    print("\n工作空间图已保存为: workspace_visualization.png")
    plt.show()


def analyze_workspace(points):
    print("\n" + "=" * 50)
    print("工作空间分析结果")
    print("=" * 50)
    
    print(f"\n采样点数: {len(points)}")
    print(f"\nX 轴范围: [{points[:, 0].min():.3f}, {points[:, 0].max():.3f}] m")
    print(f"Y 轴范围: [{points[:, 1].min():.3f}, {points[:, 1].max():.3f}] m")
    print(f"Z 轴范围: [{points[:, 2].min():.3f}, {points[:, 2].max():.3f}] m")
    
    x_range = points[:, 0].max() - points[:, 0].min()
    y_range = points[:, 1].max() - points[:, 1].min()
    z_range = points[:, 2].max() - points[:, 2].min()
    print(f"\n各轴跨度:")
    print(f"  X 轴: {x_range:.3f} m")
    print(f"  Y 轴: {y_range:.3f} m")
    print(f"  Z 轴: {z_range:.3f} m")


if __name__ == "__main__":
    points = generate_workspace_points(10000)
    analyze_workspace(points)
    plot_workspace(points)
