import mujoco
import mujoco.viewer
import time

model = mujoco.MjModel.from_xml_path("model/cable2.xml")
data = mujoco.MjData(model)

mujoco.mj_forward(model, data)

# 设置移动速度(米/秒)
speed = 0.1
start_time = time.time()
current_time = start_time
switch_time = 1

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():

        dt = time.time() - current_time
        current_time = time.time()
        if current_time - start_time > switch_time:
            speed = -speed
            start_time = current_time

        data.mocap_pos[0] += [speed * dt, 0, 0]
        data.mocap_pos[1] -= [speed * dt, 0, 0]
        mujoco.mj_step(model, data)

        viewer.sync()
