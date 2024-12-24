import mujoco
import mujoco.viewer
import time
import numpy as np

model = mujoco.MjModel.from_xml_path("model/kuka_kr20.xml")
data = mujoco.MjData(model)
mujoco.mj_step(model, data)

# 设置路径点和速度
speed = 0.5
waypoints = [
    data.xpos[model.body("cable_end").id].copy(),
    np.array([1.159, 0, 2.5]),  # 中间点
    np.array([0.16, -0, 1.6]),  # 目标点
]

current_segment = 0
distance = 0
reached = False

with mujoco.viewer.launch_passive(model, data) as viewer:
    last_time = time.time()

    while viewer.is_running():
        if not reached:
            # 更新距离
            dt = time.time() - last_time
            distance += speed * dt
            last_time = time.time()

            # 计算当前段的方向和总长度
            direction = (waypoints[current_segment + 1] -
                         waypoints[current_segment])
            segment_length = np.linalg.norm(direction)

            if distance >= segment_length:
                # 切换到下一段路径
                distance = 0
                current_segment += 1
                if current_segment >= len(waypoints) - 1:
                    reached = True
                    print("到达目标点")
                    np.savez(
                        "final_state.npz",
                        qpos=data.qpos,
                        mocap_pos=data.mocap_pos,
                    )
            else:
                # 更新位置
                new_pos = (
                    waypoints[current_segment] + direction /
                    segment_length * distance
                )
                data.mocap_pos[0] = new_pos

        mujoco.mj_step(model, data)
        viewer.sync()
