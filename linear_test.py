import Motor
import time
import threading

FIRST_WHEEL_ID = 41
FIRST_JOINT_ID = 21
NUM_WHEEL = 8
NUM_JOINT = 7

joint_motors = [Motor.Wheel_Motor(motor_id=i) for i in range(FIRST_JOINT_ID, FIRST_JOINT_ID + NUM_JOINT)]
wheel_motors = [Motor.Wheel_Motor(motor_id=i) for i in range(FIRST_WHEEL_ID, FIRST_WHEEL_ID + NUM_WHEEL)]
# 关节电机归零
for motor in joint_motors:
    motor.set_position_current_mode()
    motor.write_goal_position(2048)
time.sleep(1)

# 轮电机设置速度
for motor in wheel_motors:
    motor.set_velocity_mode()
    motor.write_goal_velocity(0)

def joint_action():
    Motor.linear_change_relative_angle(joint_motors, [30, 0, 0, 30, 0, 30, 0], 2, 0.01)
    time.sleep(2)
    Motor.linear_change_to_angle(joint_motors, [-30, 0, 0, -30, 0, -30, 0], 3, 0.01)

def wheel_actions():
    pass

joint_thread = threading.Thread(target=joint_action)
joint_thread.start()
joint_thread.join()

for motor in joint_motors:
    motor.disable_torque()