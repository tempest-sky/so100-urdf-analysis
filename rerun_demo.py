import rerun as rr
import numpy as np
import time

# 方式一：尝试自动启动 Viewer（如果成功则无需手动）
rr.init("SO-ARM100 Dynamic", spawn=True)

# 方式二：如果自动启动失败，可手动启动 Viewer 后取消下面注释
# rr.connect_grpc()

urdf_path = r"C:\Users\asus\so100_urdf\so100_with_marker.urdf"
urdf_tree = rr.urdf.UrdfTree.from_file_path(urdf_path)
rr.log_file_from_path(urdf_path, static=True)

all_joints = urdf_tree.joints()
revolute_joints = [j for j in all_joints if j.joint_type in ("revolute", "continuous")]

print("可动关节数量：", len(revolute_joints))
print("关节列表：", [j.name for j in revolute_joints])

t = 0
while True:
    for joint in revolute_joints:
        angle = 0.5 * np.sin(t)
        transform = joint.compute_transform(angle)
        rr.log("transforms", transform)
    time.sleep(0.05)
    t += 0.05