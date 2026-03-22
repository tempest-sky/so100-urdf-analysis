from yourdfpy import URDF
import numpy as np

# 加载 URDF（使用你的实际文件名）
urdf_path = r"C:\Users\asus\so100_urdf\so100_with_marker.urdf"
robot = URDF.load(urdf_path)

# 关节名称（根据打印的可用关节）
joint_names = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
# 末端连杆名称（根据打印的可用连杆）
end_link = "gripper"   # 注意：从打印结果看，末端是 "gripper"
base_link = "base"     # 基座连杆名称

print("可用连杆：", [link.name for link in robot.robot.links])
print("可用关节：", [joint.name for joint in robot.robot.joints])

def compute_fk(angles):
    """给定关节角度，计算末端相对于基座的位置和姿态"""
    cfg = dict(zip(joint_names, angles))
    # 更新机器人的配置
    robot.update_cfg(cfg)
    # 获取变换矩阵（从基座到末端）
    transform = robot.get_transform(base_link, end_link)
    pos = transform[:3, 3]
    rot = transform[:3, :3]
    return pos, rot

# 测试零位姿态
angles_zero = [0.0] * 6
pos_zero, rot_zero = compute_fk(angles_zero)
print("\n零位姿态：")
print(f"  位置 (x,y,z): {pos_zero}")
print(f"  旋转矩阵:\n{rot_zero}")

# 测试一个非零姿态（例如 shoulder_lift = 0.5 rad）
angles_pose = [0.0, 0.5, 0.0, 0.0, 0.0, 0.0]
pos_pose, rot_pose = compute_fk(angles_pose)
print("\n非零姿态 (shoulder_lift=0.5 rad)：")
print(f"  位置 (x,y,z): {pos_pose}")
print(f"  旋转矩阵:\n{rot_pose}")