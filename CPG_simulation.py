import numpy as np
import matplotlib.pyplot as plt


class SnakeRobotCPG:
    def __init__(self, num_joints, frequency, phase_offsets, time_step=0.01):
        self.num_joints = num_joints
        self.frequency = frequency
        self.phase_offsets = phase_offsets
        self.time_step = time_step
        self.program_time = 0
        self.time_steps = []
        self.control_signal_unit = [[] for _ in range(self.num_joints)]

    def update(self):
        control_signals = [
            np.sin(2 * np.pi * self.frequency * self.program_time + self.phase_offsets[i])
            for i in range(self.num_joints)
        ]
        self.time_steps.append(self.program_time)
        for i in range(self.num_joints):
            self.control_signal_unit[i].append(control_signals[i])
        self.program_time += self.time_step
        return control_signals


def simulate_snake_robot(snake_robot, iterations, color_list):
    for _ in range(iterations):
        control_signals = snake_robot.update()
        print("Control Signals:", control_signals)

    # 绘制控制信号随时间变化的图表
    for i in range(snake_robot.num_joints):
        plt.plot(snake_robot.time_steps, snake_robot.control_signal_unit[i],
                 label=f'Control Signal {i}', color=color_list[i])

    plt.xlabel('Time')
    plt.ylabel('Control Signal')
    plt.legend()
    plt.title('Control Signals over Time')
    plt.show()


# 参数设置
num_joints = 3
frequency = 1.0
phase_offsets = np.array([0, np.pi, np.pi / 3])
color_list = ['r', 'g', 'b']
iterations = 1000

# 创建蛇形机器人CPG实例
snake_robot_cpg = SnakeRobotCPG(num_joints, frequency, phase_offsets)

# 模拟并绘制图表
simulate_snake_robot(snake_robot_cpg, iterations, color_list)
