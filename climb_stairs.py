import Motor
import time
import keyboard
import threading
import numpy as np
from myTools import convert_angle, calculate_climb_stairs_angle

# 基本参数
Height = 150  # 障碍物高度 mm
Length = 180  # 蛇单模块长度 mm
# 由于本蛇的特殊性，要把两个关节当作一个关节来控制

num_wheels = 8
wheel_start_id = 21
joint_start_id = 1
joint_end_id = 9

# 定义全局标志变量，用于控制循环结束
stop_flag = False
N = 0  # 总步数
start_time = time.time()  # 获取程序开始运行的时间
last_time = start_time  # 前一次记录的时间
PROGRAM_TIME = 30  # 程序运行的总时间（秒）
INTERVAL = 0.01  # 每次移动的间隔时间（秒）
K = 11.38  # 一度对应的位置大小
next = 0
interval_time = 6  # 每次角度传递的时间间隔
motor_units_per_revolution = 4096  # 电机每圈的单位数
KI = 0.2
log_path = r"log/climb_stairs.txt"
angle_tuple = calculate_climb_stairs_angle(Height, Length)
print(angle_tuple)


# 关闭电机
def disable_all_torque(motors):
    for motor in motors:
        motor.disable_torque()


# 打开电机
def open_all_torque(motors):
    for motor in motors:
        motor.enable_torque()


# 日志函数
def log(name, lst=[], path=log_path):
    with open(path, "a", encoding="utf-8") as f:
        # 列表转字符串
        log = " ".join(map(str, lst))
        f.write(name + log + "\n")


def Init_log(log_path):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("------------------------------------------------------\n")
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")
        f.write("Height: " + str(Height) + " mm\n")
        f.write("Length: " + str(Length) + " mm\n")
        f.write("Angle: " + str(angle_tuple) + "\n")


def Wheel_init():
    # 轮
    Wheel_Motor = [
        Motor.Wheel_Motor(motor_id=i)
        for i in range(wheel_start_id, wheel_start_id + num_wheels)
    ]
    # 初始化速度,并设置轮为速度模式
    for i in range(len(Wheel_Motor)):
        Wheel_Motor[i].set_velocity_mode()
    wheel_speed = [0] * len(Wheel_Motor)
    Motor.SyncWriteVelocity(Wheel_motor=Wheel_Motor, speed=wheel_speed)
    # 所有速度设置为0
    for i in range(len(Wheel_Motor)):
        Wheel_Motor[i].write_goal_velocity(0)
    return Wheel_Motor


def Joint_init():
    # 关节
    Joint_Motor = [
        Motor.Joint_Motor(motor_id=i) for i in range(joint_start_id, joint_end_id + 1)
    ]
    # 让蛇身绷直
    for i in range(len(Joint_Motor)):
        Joint_Motor[i].set_position_current_mode()
    joint_position = [2048] * len(Joint_Motor)
    joint_position_angle = convert_angle(joint_position)
    Motor.linear_change_to_angle(Joint_Motor, joint_position_angle, 2, INTERVAL)
    return Joint_Motor


def Climb_joint_position(joint_position, next):
    # 异常处理，防止角度为空
    if angle_tuple is None:
        print("angle_tuple is None")
        return None

    # 判断是一节的情况
    elif angle_tuple[0] == 1:
        if next - 2 > len(Joint_Motor):
            joint_position = [2048] * len(Joint_Motor)
            return joint_position
        # 攀爬高台（单节）
        if next > 0:
            joint_position = [2048] * len(Joint_Motor)
            joint_position[next - 2] = int(2048 + angle_tuple[1] * K * 180 / np.pi)
        if next > len(Joint_Motor):
            return joint_position
        joint_position[next] = int(2048 - angle_tuple[1] * K * 180 / np.pi)
        if next < 4:
            joint_position[0] = int(2048 - 0.5 * K * 180 / np.pi)

        """
        # 下行功能实现（单节）
        if next > 0:
            joint_position = [2048] * len(Joint_Motor)
            ##################################################################################
            if next - 4 > 0:
                if next - 6 > len(Joint_Motor):
                    return joint_position
                joint_position[0 + next - 6] = int(
                    2048 - angle_tuple[1] * K * 180 / np.pi
                )
            if next - 2 > 0:
                if next - 4 > len(Joint_Motor):
                    return joint_position
                joint_position[0 + next - 4] = int(
                    2048 + angle_tuple[1] * K * 180 / np.pi
                )
                ##################################################################################
            if next - 2 > len(Joint_Motor):
                return joint_position
            joint_position[0 + next - 2] = int(2048 + angle_tuple[1] * K * 180 / np.pi)
        if next > len(Joint_Motor):
            return joint_position
        joint_position[0 + next] = int(2048 - angle_tuple[1] * K * 180 / np.pi)
        """

        """
        # 攀爬高台（单节）
        # 如果要更新的关节超出关节范围，则跳过
        if 0 + next >= len(Joint_Motor):
            return joint_position
        if next > 0:
            joint_position = [2048] * len(Joint_Motor)
            joint_position[0 + next - 2] = int(2048 + angle_tuple[1] * K * 180 / np.pi)
        joint_position[0 + next] = int(2048 - angle_tuple[1] * K * 180 / np.pi)
        """

        """
        # 攀爬楼梯（单节）
            if 0 + next >= len(Joint_Motor):
                return joint_position
            if next > 0:
                for a in range(next // 2 + 1):
                if joint_position[a * 2] < 2048:
                    joint_position[a * 2] = int(2048 + angle_tuple[1] * K * 180 / np.pi)
                elif joint_position[a * 2] > 2048:
                    joint_position[a * 2] = int(2048 - angle_tuple[1] * K * 180 / np.pi)
                else:
                    joint_position[a * 2] = int(2048 - angle_tuple[1] * K * 180 / np.pi)
        """

    # 多节的情况
    elif angle_tuple[0] > 1:
        """
        # 攀爬高台（多节）
        # 如果要更新的关节超出关节范围，则跳过
        if 0 + next >= len(Joint_Motor):
            joint_position = [2048] * len(Joint_Motor)
            return joint_position
        # 上一节角度变为当前关节角度
        if next > 0:
            joint_position = [2048] * len(Joint_Motor)
            joint_position[0 + next - 2] = int(2048 + angle_tuple[1] * K * 180 / np.pi)
        # 下一节角度变为当前关节角度
        joint_position[0 + next] = int(2048 + angle_tuple[1] * K * 180 / np.pi)
        for i in range(angle_tuple[0] - 1):
            if 2 + i * 2 + next >= len(Joint_Motor):
                break
            joint_position[2 + i * 2 + next] = int(
                2048 - angle_tuple[2] * K * 180 / np.pi
            )
        """

        # 攀爬（多节）
        if next - 6 > len(Joint_Motor):
            joint_position = [2048] * len(Joint_Motor)
            return joint_position

        joint_position = [2048] * len(Joint_Motor)

        if next > 0:
            if next - 4 > 0:
                if next - 6 < len(Joint_Motor):
                    joint_position[next - 6] = int(2048 - angle_tuple[1] * K * 180 / np.pi)
            if next - 2 > 0:
                if next - 4 < len(Joint_Motor):
                    joint_position[next - 4] = int(2048 + angle_tuple[1] * K * 180 / np.pi)
            if next - 2 < len(Joint_Motor):
                joint_position[next - 2] = int(2048 + angle_tuple[1] * K * 180 / np.pi)

        for i in range(angle_tuple[0] - 1):
            if next + 2 + i * 2 >= len(Joint_Motor):
                break
            joint_position[next + 2 + i * 2] = int(2048 - angle_tuple[2] * K * 180 / np.pi)

        if next < len(Joint_Motor):
            joint_position[next] = int(2048 - angle_tuple[1] * K * 180 / np.pi)

    return joint_position


# 爬行
def Crawl_straight(Wheel_Motor, Joint_Motor, joint_position):
    open_all_torque(Wheel_Motor)
    wheel_speed_single = 200
    pid_output = [wheel_speed_single] * len(Wheel_Motor)
    ##################################################################################
    # 控制前进代码
    Motor.SyncWriteVelocity(Wheel_motor=Wheel_Motor, speed=pid_output)
    time.sleep(interval_time * 0.7)
    ##################################################################################
    print(pid_output)
    log("轮子：", pid_output)
    disable_all_torque(Wheel_Motor)

def stop_all_motor(Wheel_Motor, Joint_Motor):
    while True:
        if keyboard.is_pressed("e"):  # 按下e程序停止运行
            # 程序结束，关闭所有电机力矩
            global stop_flag
            stop_flag = True
            disable_all_torque(Joint_Motor)
            disable_all_torque(Wheel_Motor)
            print("Stop the Program")
            log("程序结束")
            break

Init_log(log_path)
Wheel_Motor = Wheel_init()
Joint_Motor = Joint_init()
joint_position = [2048] * len(Joint_Motor)
# open_all_torque(Wheel_Motor)
# wheel_speed_single = 150
# pid_output = [wheel_speed_single] * len(Wheel_Motor)
# 控制前进代码
# Motor.SyncWriteVelocity(Wheel_motor=Wheel_Motor, speed=pid_output)

thread1 = threading.Thread(target=stop_all_motor, args=(Wheel_Motor, Joint_Motor))
thread1.start()
thread1.join()

while not stop_flag:
    current_time = time.time()  # 获取当前时间
    elapsed_time = current_time - start_time  # 计算程序已经运行的时间

    if elapsed_time >= PROGRAM_TIME:  # 如果程序已经运行了xx秒，就跳出循环
        break
    ##########################################################################################
    # 控制前进代码
    if current_time - last_time > interval_time:  # 轮子
        last_time = current_time
        Crawl_straight(Wheel_Motor, Joint_Motor, joint_position)
        next += 2
    ##########################################################################################
    joint_position = Climb_joint_position(joint_position, next)
    if joint_position == None:
        print("joint_position is none")
        break
    joint_position_angle = convert_angle(joint_position)
    ##########################################################################################
    # 控制关节转动代码
    Motor.linear_change_to_angle(
        Joint_Motor, joint_position_angle, interval_time * 0.3, INTERVAL
    )
    ##########################################################################################
    log("关节：", joint_position_angle)
    print(joint_position_angle)
    # print(joint_position)
    # time.sleep(2)
    N += 1

    present_position = Motor.SyncReadPosition(Joint_Motor)
    difference = [0] * len(Joint_Motor)
    current = [0] * len(Joint_Motor)
    for i in range(len(Joint_Motor)):
        difference[i] = joint_position[i] - present_position[i]
        current[i] = int(KI * difference[i])
    # print(current)
