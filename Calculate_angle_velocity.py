import numpy as np
import math


def calculate_climb_stairs_angle(height: float, length: float) -> tuple:
    if height <= length:
        phi_a = math.asin(height / length)
        # 抬起高度小于三十度，统一变成三十度，设置下限
        if phi_a < math.asin(1 / 2):
            phi_a = math.asin(1 / 2)
        return (1, np.around(phi_a, decimals=2))

    else:
        phi_a = 75 / 180 * np.pi  # 一般取90/np.pi，是轴关节的极限角度
        n = height / (length * np.abs(np.sin(phi_a)))  # 角度为 phi_a 的关节个数
        n = math.floor(n)
        phi_c = math.asin(
            (height - n * length * np.abs(np.sin(phi_a))) / length
        )  # 最后一个关节的弧度
        phi_b = phi_a - phi_c  # 倒数第二个关节的弧度
        # 总共 n+1 个关节悬空
        return (n + 1, np.around(phi_b, decimals=2), np.around(phi_a, decimals=2))


def calculate_climb_stairs_velocity(
        length: float, joint_angular_velocity: float, angle_tuple: tuple
) -> float:
    return (
            joint_angular_velocity
            * length
            / np.abs(np.sin(angle_tuple[len(angle_tuple) - 1]))
    )


if __name__ == "__main__":
    a = calculate_climb_stairs_angle(250, 180)  # mm
    print(a)
