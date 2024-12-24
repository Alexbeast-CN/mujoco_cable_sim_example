# Mujoco 线缆仿真

本项目使用 Mujoco 物理引擎实现工业机器人线缆的物理仿真，探索线缆在机器人运动过程中的物理行为。

最终效果：

![](media/robot_cable.mp4)

文件说明：

1. `model/cable.xml` - 线缆仿真模型
2. `model/kuka_kr20.xml` - 机器人模型
3. `run_robot.py` - 机器人关节控制
4. `move2target.py` - 线缆末端运动到目标点
5. `get_body_pos.py` - 获取 kuka_kr20 机器人中指定构件位置
6. `view.py` - 仿真场景可视化

