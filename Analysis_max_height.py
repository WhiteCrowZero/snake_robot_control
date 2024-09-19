import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置中文字体为SimHei
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 定义参数
B = 180.00  # 机器人模块长度 (mm)
R = 28.00     # 机器人半径 (mm)
Upper_Angle_Limit = 75  # 机器人仰角上限 (度)


def Analysis_of_maximum_obstacle_ability_single(B:float,R:float)-> tuple:
    # 定义仰角θ的范围（0度到70度）
    theta = np.linspace(0, Upper_Angle_Limit, 100)  # 角度的范围从0到70度，分100个点

    # 计算每个θ对应的H值
    theta_rad = np.radians(theta)  # 将角度转换为弧度
    # print(theta_rad)
    H = (B / 2) * np.sin(theta_rad) + R * (1 - 1 / np.cos(theta_rad))
    
    max_height = -1
    max_theta = -1
    for a,b in zip(theta,H):
        if b > max_height:
            max_height = b
            max_theta = a
    
    # 单个机器人模块最大高度对应的仰角和最大高度
    return tuple(np.around((max_theta,max_height), decimals=2))


def plot_max_height(B:float,R:float):
    # data
    theta = np.linspace(0, Upper_Angle_Limit, 100)  # 角度的范围从0到70度，分100个点
    theta_rad = np.radians(theta)  # 将角度转换为弧度
    H = (B / 2) * np.sin(theta_rad) + R * (1 - 1 / np.cos(theta_rad))
    baseline = [0]*len(theta)
    (max_theta,max_height) = Analysis_of_maximum_obstacle_ability_single(B,R)
    
    # 绘制图形
    plt.figure(figsize=(8, 6))
    plt.plot(theta, H, label='障碍物高度 H')
    plt.plot(theta, baseline, label='机器人底面')
    plt.plot(max_theta, max_height, 'ro', label=f'最大高度点({max_theta:.2f}, {max_height:.2f})')
    
    # 添加标题和标签
    plt.title('机器人重心在行进方向上经过A点时的障碍物高度 H 和机器人仰角 θ 的关系')
    plt.xlabel('机器人仰角 θ (度)')
    plt.ylabel('障碍物高度 H (mm)')
    plt.legend()

    # 显示网格
    plt.grid(True)

    # 显示图形
    plt.show()

def Analysis_of_maximum_obstacle_ability_all(B:float,R:float,A:float,N:int):
    all_max = (B+2*A)*(N-1)/2
    return all_max

if __name__ == '__main__':
    single_max = Analysis_of_maximum_obstacle_ability_single(B,R)
    print(single_max)
    
    plot_max_height(B,R)
    
    A = 22.5 # 弯举舵机摆臂转动轴到弯举舵机配合平面的距离 或 机器人后轮轴心到机器人连接器配合平面的距离(mm)
    N = 4 # 机器人模块数，一般为奇数
    all_max = Analysis_of_maximum_obstacle_ability_all(B,R,A,N)
    print(f'机器人模块数为 {N} 时的最大高度为 {all_max:.2f} mm')



