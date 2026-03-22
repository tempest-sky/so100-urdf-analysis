import time
import numpy as np
from yourdfpy import URDF

urdf_path = r"C:\Users\asus\so100_urdf\so100_with_marker.urdf"
robot = URDF.load(urdf_path)

joint_names = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
base_link = "base"
end_link = "gripper"

t = 0
while True:
    # 正弦轨迹：每个关节以不同相位运动
    angles = [
        0.5 * np.sin(t),           # shoulder_pan
        0.3 * np.sin(t + 1),       # shoulder_lift
        0.2 * np.sin(t + 2),       # elbow_flex
        0.1 * np.sin(t + 3),       # wrist_flex
        0.1 * np.sin(t + 4),       # wrist_roll
        0.0                        # gripper 保持闭合
    ]
    cfg = dict(zip(joint_names, angles))
    robot.update_cfg(cfg)
    transform = robot.get_transform(base_link, end_link)
    pos = transform[:3, 3]
    print(f"时间 {t:.2f}: 末端位置 ({pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f})")
    time.sleep(0.2)
    t += 0.2