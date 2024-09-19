## 1. **Introduction**
This is a motor control library based on the official Python Dynamixel SDK, designed to simplify control operations.

## 2. **Installation and Configuration**
   - Install the Dynamixel Python SDK: 
     ```bash
     pip install dynamixel_sdk
     ```
   - Modify the `Parameters.py` file to set `DEVICENAME` (port) and `BAUDRATE` (baud rate) to establish a connection with the motor.

## 3. **Basic Motor Control**
   - Create a motor object
   - Enable motor and switch modes:
     - Enable torque, switch between velocity and position modes.
   - Set speed and position:
     - In velocity mode, set speed.
     - In position mode, set the position (2048 represents 0 degrees, 4096 represents +180 degrees, 0 represents -180 degrees).

## 4. **Synchronized Control**
   - Perform synchronized control of multiple motors:
     - Synchronously set the speed and position of multiple motors.
     - Example: 
     ```python
     SyncWriteVelocity(wheelMotors, [200, 100, 200, 100])
     ```
     - Example for reading positions:
     ```python
     Positions = SyncReadPosition(wheelMotors)
     ```

## 5. **Core Code Logic**
   - Control motors by writing values to specific addresses.
   - Example code for enabling torque:
     ```python
     Wheel_packetHandler.write1ByteTxRx(portHandler, self.motor_id, Parameters.ADDR_TORQUE_ENABLE, 1)
     ```
   - Synchronized writing process is simplified in three steps: add parameters to the buffer, transmit parameters, clear the buffer.
