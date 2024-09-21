import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

"""
CPG（Central Pattern Generator，中枢模式发生器）概述：
1. 简介
CPG（Central Pattern Generator，中枢模式发生器）算法是一种仿生学算法，模拟生物体内用于产生周期性运动模式的神经网络结构。CPG 本质上是能够自主生成节律性输出信号（如步态、呼吸等）的神经元网络，常用于机器人学中的运动控制，特别是蛇形机器人、四足机器人等有周期性运动模式的机器体。
2. CPG 算法的核心组成：
振荡器（Oscillator）：每个关节或运动单元通常使用一个振荡器来生成周期性信号（通常是正弦或余弦波）。
相位偏移（Phase Offset）：不同振荡器之间通常有一定的相位差，这样可以使不同关节之间的运动协调。
频率（Frequency）：控制整个系统的运动节奏，通过调节频率可以加快或减慢运动速度。
耦合机制：各振荡器之间往往通过某种耦合机制互相作用，从而协调多个关节的运动，使得整体动作更加自然流畅。
"""

# CPG 微分方程
def cpg_system(time, state, convergence_rate, output_amplitude, swing_freq, transition_speed, duty_cycle,
               coupling_strength, coupling_values):
    # 计算振荡频率 w
    stance_freq = swing_freq * (1 - duty_cycle) / duty_cycle
    oscillation_freq = stance_freq / (math.exp(-transition_speed * state[1]) + 1) + swing_freq / (
                math.exp(transition_speed * state[1]) + 1)

    # 计算状态的变化率（加入耦合和动态调节机制）
    dx1dt = convergence_rate * (output_amplitude - state[0] ** 2 - state[1] ** 2) * state[0] - oscillation_freq * state[
        1]
    dx2dt = convergence_rate * (output_amplitude - state[0] ** 2 - state[1] ** 2) * state[1] + oscillation_freq * state[
        0] + coupling_strength * (
                    -coupling_values[0] * math.sin(2) + coupling_values[1] * math.sin(2))  # 耦合项

    return [dx1dt, dx2dt]


class SnakeRobotCPG:
    def __init__(self, num_joints, base_frequency, phase_offsets, time_step=0.01):
        self.num_joints = num_joints
        self.base_frequency = base_frequency
        self.phase_offsets = phase_offsets
        self.time_step = time_step
        self.program_time = 0
        self.time_steps = []
        self.control_signals_per_joint = [[] for _ in range(self.num_joints)]
        self.NORMALIZATION_FACTOR = 0.1465  # 归一化常量

        # 初始化 CPG 状态，每个关节都有两个变量 x0 和 x1
        self.joint_states = [[1, 0] for _ in range(self.num_joints)]  # 初始条件
        self.convergence_rate = 100  # 收敛速度
        self.output_amplitude = 1.0  # 输出信号的幅值
        self.swing_freq = math.pi  # 摆动相频率
        self.transition_speed = 1  # 在摆动与支撑之间变化的速度
        self.duty_cycle = 0.5  # 占空比
        self.coupling_strength = 0.6  # 耦合强度
        self.max_angle = 60.0 * self.NORMALIZATION_FACTOR  # 最大关节角度

    def update(self):
        control_signals = []
        for joint_idx in range(self.num_joints):
            # 耦合参数：当前关节与前一关节的状态
            if joint_idx == 0:
                coupling_values = [0, 0]  # 第一个关节没有耦合
            else:
                coupling_values = [self.joint_states[joint_idx - 1][0], self.joint_states[joint_idx - 1][1]]

            # 使用 solve_ivp 求解 CPG 微分方程
            sol = solve_ivp(cpg_system, [self.program_time, self.program_time + self.time_step],
                            self.joint_states[joint_idx],
                            args=(self.convergence_rate, self.output_amplitude, self.swing_freq,
                                  self.transition_speed, self.duty_cycle, self.coupling_strength, coupling_values))

            # 更新关节状态
            self.joint_states[joint_idx] = [sol.y[0][-1], sol.y[1][-1]]

            # 将控制信号从 CPG 状态映射为角度
            joint_angle = int(sol.y[1][0] * self.max_angle / self.NORMALIZATION_FACTOR)
            control_signals.append(joint_angle)
            self.control_signals_per_joint[joint_idx].append(joint_angle)

        self.time_steps.append(self.program_time)
        self.program_time += self.time_step

        return control_signals


def simulate_snake_robot(snake_robot, iterations, color_list):
    for _ in range(iterations):
        control_signals = snake_robot.update()
        print("Control_Signals:", control_signals)

    # 绘制控制信号随时间变化的图表
    for joint_idx in range(snake_robot.num_joints):
        plt.plot(snake_robot.time_steps, snake_robot.control_signals_per_joint[joint_idx],
                 label=f'Control_Signal {joint_idx}', color=color_list[joint_idx])

    plt.xlabel('Time')
    plt.ylabel('Control_Signal')
    plt.legend()
    plt.title('Control Signals over Time')
    plt.show()

if __name__ == '__main__':
    # 测试代码
    num_joints = 3
    base_frequency = 1.0
    phase_offsets = np.array([0, np.pi, np.pi / 3])  # 引入相位差
    snake_robot_cpg = SnakeRobotCPG(num_joints, base_frequency, phase_offsets)

    # 模拟蛇形机器人关节运动并绘图
    color_list = ['r', 'g', 'b']
    simulate_snake_robot(snake_robot_cpg, 1000, color_list)
