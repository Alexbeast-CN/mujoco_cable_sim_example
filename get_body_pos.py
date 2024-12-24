import mujoco
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="获取机器人body位置")
    parser.add_argument(
        "-b", "--body_name",
        type=str,
        default="cable_B_last",
        help="需要查询位置的body名称 (默认: cable_B_last)",
    )
    return parser.parse_args()


def main():
    args = get_args()

    model = mujoco.MjModel.from_xml_path("model/kuka_kr20.xml")
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    try:
        body_id = model.body(args.body_name).id
        print(f"{args.body_name}的位置: {data.xpos[body_id]}")
    except KeyError:
        print(f"错误: 找不到名为 '{args.body_name}' 的body")


if __name__ == "__main__":
    main()
