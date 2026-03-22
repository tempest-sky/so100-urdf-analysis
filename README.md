# SO-ARM100 机械臂 URDF 结构分析

## 项目概述

- **目标**：学习机器人 URDF（统一机器人描述格式）的核心结构，理解关节、连杆、运动学参数的表示方法。
- **URDF 来源**：[TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) 仓库中的 urdf/so100.urdf
- **使用工具**：
    - Python + yourdfpy 加载并解析 URDF
    - Foxglove Studio（可选）进行可视化
    - VS Code 编辑 XML 文件

## 一、URDF 文件概览

- **文件名**：so100.urdf
- **文件大小**：\___ KB
- **主要内容**：定义了 \___ 个连杆、\___ 个关节（包括 \___ 个旋转关节、\___ 个固定关节）
- **依赖资源**：引用了 assets/ 文件夹下的 STL 模型文件（如 Base.stl 等），但学习时缺失不影响结构分析

## 二、关节（Joint）分析

使用 Python 加载并打印所有关节信息：

python

from  
robot = URDF.load("so100.urdf")  
for joint in robot.robot.joints:  
print(joint.name, joint.type)

### 输出结果（实际运行结果粘贴在这里）：

text

shoulder_pan  
shoulder_lift revolute  
elbow_flex revolute  
wrist_flex revolute  
wrist_roll revolute  
gripper revolute  
...

### 关键关节详细记录（至少 3 个）

| 关节名称 | 类型  | 轴方向 (xyz) | 运动范围 (lower, upper) | 作用  |
| --- | --- | --- | --- | --- |
| shoulder_pan | revolute | (0, 0, 1) | (-2.5, 2.5) rad | 腰部旋转 |
| shoulder_lift | revolute | (0, 1, 0) | (-2.0, 2.0) rad | 肩部俯仰 |
| elbow_flex | revolute | (0, 1, 0) | (-1.5, 1.5) rad | 肘部弯曲 |
| …   | …   | …   | …   | …   |

**注**：具体数值以 URDF 文件中的 &lt;limit&gt; 标签为准。

## 三、连杆（Link）分析

URDF 中定义了多个连杆，每个连杆包含视觉、碰撞和惯性信息。下面列出几个关键连杆：

| 连杆名称 | 视觉几何 | 碰撞几何 | 惯性参数 |
| --- | --- | --- | --- |
| base_link | assets/Base.stl | assets/Base.stl | mass=0.5, inertia≈… |
| upper_arm_link | assets/Upper_Arm.stl | assets/Upper_Arm.stl | …   |
| forearm_link | assets/Lower_Arm.stl | assets/Lower_Arm.stl | …   |
| …   | …   | …   | …   |

### 补充：缺少 mesh 文件的影响

- 由于未下载 assets/ 文件夹，Python 加载时出现 Unable to resolve filename 警告，但关节信息依然完整。
- 如果需要完整可视化，可下载整个仓库并保持相对路径一致。

## 四、运动学链结构

机械臂的运动学链可以简化为以下顺序（从基座到末端）：

text

base_link

每个关节的相对变换通过

例如，shoulder_pan 相对于 base_link 的变换为：

xml

&lt;origin xyz="0 0 0.1" rpy="0 0 0"/&gt;

## 五、实践尝试：修改关节参数

### 尝试 1：修改连杆颜色（需可视化支持）

- 找到某个 &lt;visual&gt; 下的 &lt;color&gt; 标签，将 rgba 改为 "1 0 0 1"（红色）。
- 保存后重新加载，观察颜色变化。（由于缺少 mesh 文件，此修改在纯结构分析中不可见，但可体现对 URDF 语法的理解）

### 尝试 2：修改关节限位

- 将 shoulder_pan 的 &lt;limit upper="2.5"/&gt; 改为 1.5。
- 用 Python 重新加载并打印该关节的 limit.upper，验证修改生效：

python

joint  
print(joint.limit.upper)

## 六、遇到的问题及解决

- **问题**：Foxglove Studio 打开 URDF 时报错 Unsupported extension: 'urdf'。
- **解决**：改用 Python 的 yourdfpy 库进行结构分析，或使用在线 URDF 查看器。
- **问题**：Python 加载时提示找不到 STL 文件。
- **解决**：这不是致命错误，因为结构信息仍可读取。若需可视化，可手动下载 assets 文件夹。

## 七、总结与后续计划

- **收获**：掌握了 URDF 中 &lt;joint&gt; 和 &lt;link&gt; 的核心语法，理解了机器人运动学链的表示方法。
- **后续计划**：
    1.  尝试使用 Python 控制关节角度，模拟简单运动。
    2.  在 LeRobot 框架中加载此 URDF，结合仿真环境进行简单的轨迹规划。
    3.  将本项目的分析过程整理为博客，加深理解。

## 附录：项目文件结构

text

C:\\Users\\asus\\so100_urdf/  
├── so100.urdf # URDF 文件  
├── assets/ # （可选）3D 模型文件  
├── README.md # 本分析笔记  
└── code/ # （可选）Python 脚本

**日期**：2026年3月  
**作者**：$$你的名字$$  
**GitHub 仓库**：$$你的仓库链接$$