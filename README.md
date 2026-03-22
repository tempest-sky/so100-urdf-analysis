![Python](https://img.shields.io/badge/Python-3.10-blue)![License](https://img.shields.io/badge/License-MIT-green)![Status](https://img.shields.io/badge/Status-Active-brightgreen)![yourdfpy](https://img.shields.io/badge/yourdfpy-0.1.0-orange)![GitHub last commit](https://img.shields.io/github/last-commit/tempest-sky/so100-urdf-analysis)
# SO-ARM100 机械臂 URDF 结构分析

## 项目概述

- **目标**：学习机器人 URDF（统一机器人描述格式）的核心结构，理解关节、连杆、运动学参数的表示方法。
- **URDF 来源**：[TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) 仓库中的 urdf/so100.urdf
- **使用工具**：
    - Python + yourdfpy 加载并解析 URDF
    - Foxglove Studio（可选）进行可视化
    - VS Code 编辑 XML 文件

## 一、URDF 文件概览

- **文件名**：so100.urdf
- **文件大小**：9 KB
- **主要内容**：定义了 7个连杆、6 个关节（全部为旋转关节，无固定关节）
- **依赖资源**：引用了 assets/ 文件夹下的 STL 模型文件（如 Base.stl 等），但学习时缺失不影响结构分析

## 二、关节（Joint）分析

使用 Python 加载并打印所有关节信息：

python

from  
robot = URDF.load("so100.urdf")  
for joint in robot.robot.joints:  
print(joint.name, joint.type)

### 输出结果（实际运行结果粘贴在这里）：

text

shoulder_pan		revolute
shoulder_lift		revolute
elbow_flex		revolute
wrist_flex		revolute
wrist_roll		revolute
gripper		revolute
### 关键关节详细记录（至少 3 个）

| 关节名称 | 类型  | 轴方向 (xyz) | 运动范围 (lower, upper) | 作用  |
| --- | --- | --- | --- | --- |
| shoulder_pan | revolute | (0, 1, 0) | (-2, 2) rad | 腰部旋转 |
| shoulder_lift | revolute | (1, 0, 0) | (0, 3.5) rad | 肩部俯仰 |
| elbow_flex | revolute | (1, 0, 0) | (-3.142, 0) rad | 肘部弯曲 |
| wrist_flex  |  revolute  | (1, 0, 0) | （-2.5, 1.2） rad  |腕部俯仰 |
| wrist_roll | revolute | (0, 1, 0) | (-3.142, 3.142) rad | 腕部旋转 |
|  gripper | revolute | (0, 0, 1) | (-0.2, 2) rad | 夹爪开合 |


## 三、连杆（Link）分析

URDF 中定义了多个连杆，每个连杆包含视觉、碰撞和惯性信息。下面列出几个关键连杆：

| 连杆名称 | 视觉几何 | 碰撞几何 | 惯性质量(kg) |
| --- | --- | --- | --- |
| base_link | assets/Base.stl | assets/Base.stl | 1.0|
|  shoulder_link | assets/Rotation_Pitch.stl | assets/Rotation_Pitch.stl | 0.119226   |
| upper_arm_link | assets/Upper_Arm.stl | assets/Upper_Arm.stl |  0.162409  |
| lower_arm_link   | assets/Lower_Arm.stl  | assets/Lower_Arm.stl   | 0.147968   |
| wrist_link   | assets/Wrist_Pitch_Roll.stl  | assets/Wrist_Pitch_Roll.stl  | 0.0661321   |
|gripper_link   | assets/Fixed_Jaw.stl  | 无碰撞几何  |  0.0929859   |
|jaw_link   | assets/Moving_Jaw.stl  | 无碰撞几何  |  0.0202444   |
### 补充：缺少 mesh 文件的影响

- 未下载 assets/ 文件夹，Python 加载时出现 Unable to resolve filename 警告，但关节信息依然完整。
- 如果需要完整可视化，可下载整个仓库并保持相对路径一致。

## 四、运动学链结构

机械臂的运动学链可以简化为以下顺序（从基座到末端）：

graph LR
    base -->|shoulder_pan| shoulder
    shoulder -->|shoulder_lift| upper_arm
    upper_arm -->|elbow_flex| lower_arm
    lower_arm -->|wrist_flex| wrist
    wrist -->|wrist_roll| gripper
    gripper -->|gripper| jaw

## 五、实践尝试：修改关节参数

### 尝试 1：修改连杆颜色（需可视化支持）

## 💡 实践尝试

### 1️⃣ 修改关节限位
- 将 `shoulder_pan` 关节的 `upper` 限位从 `2.0 rad` 改为 `1.0 rad`。
- 通过 Python 重新加载 URDF，验证限位已更新：
  ```python
  joint = [j for j in robot.robot.joints if j.name == 'shoulder_pan'][0]
  print(joint.limit.upper)  # 输出 1.0
 - **目的**：验证 URDF 中关节限位对运动范围的影响。
- **步骤**：修改 `shoulder_pan` 上限，重新加载并打印限位值。
- **结果**：成功修改，证明了对 `<limit>` 标签的理解正确。
- **延伸思考**：如果限位设置过小，会导致机械臂无法到达某些工作空间位置。

### 🎨 修改连杆颜色
- **目标**：理解 URDF 中视觉材质的定义方式，将 `base_link` 的视觉颜色改为红色。
- **操作**：在 URDF 的 `<visual>` 中将 `<color rgba="0.7 0.7 0.7 1.0"/>` 修改为 `"1.0 0.0 0.0 1.0"`。
- **验证**：重新加载 URDF，通过 Python 打印颜色值确认修改成功；若拥有 mesh 文件，可在 Foxglove 中直观看到变化。
- **收获**：掌握了 URDF 中视觉材质的定义与修改方法。
- **步骤**：修改 `base_link` 的 `<color>` 值，通过 Python 读取确认属性变化。
- **局限**：因缺少 mesh 文件无法在 Foxglove 中直接观察，但验证了代码层面修改的有效性。


### 3. 添加虚拟连杆

- **操作**：在 URDF 中增加红色球体连杆 `marker_link`，并通过固定关节固定在 `base_link` 上。
- **验证**：使用 Python 加载新 URDF，确认连杆和关节均成功添加，父-子关系正确。
- **意义**：掌握了扩展 URDF 模型的方法，为后续自定义机器人模型打下基础。

### 4. 正运动学验证脚本
- **目标**：给定关节角度，计算末端位置。
- **实现**：编写 Python 脚本，使用 `yourdfpy.link_fk()`。
- **结果**：零位时末端坐标为 (0.XX, 0.XX, 0.XX)，与理论值一致。
### 🤖 正运动学验证

使用 `yourdfpy` 编写脚本 `fk_test.py`，给定关节角度，计算末端执行器（`gripper`）相对于基座（`base`）的位置和姿态。

**零位姿态**（所有关节角度为0）：
- 位置：`(0.1775, 0.0925, -0.0000)` m
- 旋转矩阵：[[ 6.32679490e-06  3.34976228e-01 -9.42226579e-01]
 [ 0.00000000e+00  9.42226579e-01  3.34976228e-01]
 [ 1.00000000e+00 -2.11932589e-06  5.96127431e-06]]

**非零姿态**（`shoulder_lift=0.5 rad`）：
- 位置：`(0.1758, 0.0227, -0.0000)` m
- 旋转矩阵：[[ 6.32679490e-06  7.45696781e-01 -6.66285457e-01]
 [ 0.00000000e+00  6.66285457e-01  7.45696781e-01]
 [ 1.00000000e+00 -4.71787059e-06  4.21545143e-06]]

**结论**：末端位姿随关节角度变化符合运动学规律，验证了 URDF 模型的正确性。该脚本可为后续轨迹规划提供基础。
### 5. LeRobot 仿真运动
- **目标**：动态改变关节角度，模拟末端轨迹。
- **实现**：编写循环，生成正弦运动，实时打印末端位置。
- **结果**：末端位置随时间周期性变化，验证了运动学链的连续性。
### 🎬 连续运动仿真
- **脚本**：`leRobot_sim.py`
- **功能**：通过正弦信号驱动各关节，实时计算并打印末端位置轨迹。
- **结果**：末端位置随时间周期性变化，验证了关节空间到笛卡尔空间的映射。
- **意义**：为后续轨迹规划与控制提供了基础示例。
## ⚠️ 注意事项

### 1. 添加虚拟连杆
- **XML 语法**：修改 URDF 时确保标签正确闭合，避免出现未配对标签。
- **路径管理**：若修改后的 URDF 与原始文件在同一目录，加载时直接使用文件名；若移动位置，需使用绝对路径。
- **惯性参数**：添加的虚拟连杆虽不影响运动学，但建议设置合理的惯性值（如质量极小），避免动力学仿真报错。

### 2. 运动学验证脚本
- **末端连杆名称**：不同 URDF 中末端执行器连杆名可能不同（如 `gripper_link`、`end_effector_link`）。使用前可先打印所有连杆名：`[link.name for link in robot.robot.links]`。
- **关节顺序**：`link_fk()` 需要关节角度字典，键名必须与 URDF 中的关节名完全一致（包括大小写）。
- **坐标参考系**：`link_fk()` 返回的变换矩阵是相对于世界坐标系的，若需要相对于基座坐标系，可额外计算。

### 3. LeRobot 仿真运动
- **环境依赖**：确保 `yourdfpy` 已安装（`pip install yourdfpy`），且 Python 版本 ≥ 3.8。
- **实时打印**：若打印频率过高导致终端刷屏，可增加 `time.sleep()` 间隔或限制输出行数。
- **终止运行**：在终端按 `Ctrl+C` 可安全停止循环。

### 4. 通用建议
- **版本控制**：所有修改建议使用 Git 管理，方便回溯和对比。
- **文档更新**：每次修改后及时更新 README，记录变更目的和验证结果。
- **测试环境**：推荐在独立的虚拟环境（如 `lerobot`）中进行实验，避免影响其他项目。

## 六、🔍遇到的问题及解决


1. **问题**：Foxglove Studio 无法直接打开 URDF 文件。
   **解决**：改用 Python 的 `yourdfpy` 库进行结构解析，并通过代码验证模型正确性。

2. **问题**：URDF 中部分连杆缺少 mesh 文件导致警告。
   **解决**：通过代码过滤警告，专注于关节与连杆的结构信息；同时学习 URDF 对视觉文件的引用机制。



## 七、总结与后续计划

- **收获**：掌握了 URDF 中 &lt;joint&gt; 和 &lt;link&gt; 的核心语法，理解了机器人运动学链的表示方法。
- **后续计划**：
    1.  尝试使用 Python 控制关节角度，模拟简单运动。
    2.  在 LeRobot 框架中加载此 URDF，结合仿真环境进行简单的轨迹规划。

      
