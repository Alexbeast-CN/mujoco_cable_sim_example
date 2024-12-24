import mujoco
import mujoco.viewer
import numpy as np
import os
from pynput import keyboard
import time

# 加载机器人模型
model = mujoco.MjModel.from_xml_path("model/kuka_kr20.xml")
data = mujoco.MjData(model)

# 加载保存的状态
if os.path.exists("final_state.npz"):
    saved_state = np.load("final_state.npz")
    data.qpos[:] = saved_state["qpos"]
    data.mocap_pos[:] = saved_state["mocap_pos"]
    mujoco.mj_step(model, data)
else:
    print("未找到状态文件")
    exit()

# 控制标志
run = False


def on_press(key):
    global run
    run = True


# 启动键盘监听
listener = keyboard.Listener(on_press=on_press)
listener.start()

# 仿真主循环
angle = 0  # 旋转角度
speed = 5  # 旋转速度
time_step = 0.01

print("按任意键开始运动...")

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running() and angle < 60:  # 限制最大旋转角度为50
        if run:
            # 更新关节角度
            angle += speed * time_step  # 使用固定的时间步长
            data.ctrl[4] = angle
            data.ctrl[2] = angle

        # 更新仿真
        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(time_step)

listener.stop()
