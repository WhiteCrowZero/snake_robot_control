import Motor
import time
import keyboard
from myTools import convert_angle

num_wheels = 8
wheel_start_id = 21
joint_start_id = 1
joint_end_id = 9
log_path = r"log/wheel_log.txt"
interval_time = 2
INTERVAL = 0.01
PROGRAM_TIME = 20

# 关闭电机
def disable_all_torque(motors):
    for motor in motors:
        motor.disable_torque()

# 打开电机
def open_all_torque(motors):
    for motor in motors:
        motor.enable_torque()

# 日志函数
def log(name, lst, path=log_path):
    with open(path, "a", encoding="utf-8") as f:
        # 列表转字符串
        log = " ".join(map(str, lst))
        f.write(name + log + "\n")

def Init_log(log_path):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("------------------------------------------------------\n")
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")

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
    # 控制关节转动代码
    Motor.linear_change_to_angle(
        Joint_Motor, joint_position_angle, interval_time, INTERVAL
    )
    log("关节：", joint_position_angle)
    return Joint_Motor

Init_log(log_path)
Wheel_Motor = Wheel_init()
Joint_Motor = Joint_init()

open_all_torque(Wheel_Motor)
wheel_speed_single = 150
pid_output = [wheel_speed_single] * len(Wheel_Motor)

# 控制前进代码
Motor.SyncWriteVelocity(Wheel_motor=Wheel_Motor, speed=pid_output)
print(pid_output)
log("轮子：", pid_output)


start_time = time.time()  # 获取程序开始运行的时间
while True:

    if keyboard.is_pressed("e"):  # 按下e程序停止运行
        break

    end_time = time.time()
    if end_time - start_time > PROGRAM_TIME:
        break


# 程序结束，关闭所有电机力矩
print("Stop the Program")
disable_all_torque(Joint_Motor)
disable_all_torque(Wheel_Motor)
