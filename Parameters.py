# Control table address for PRO model Dynamixel
ADDR_PRO_TORQUE_ENABLE = 64  # Control table address for enabling torque
ADDR_PRO_GOAL_POSITION = 116  # Control table address for goal position
ADDR_PRO_PRESENT_POSITION = 132  # Control table address for present position
ADDR_PRO_GOAL_VELOCITY = 104  # Control table address for goal velocity
ADDR_PRO_PRESENT_VELOCITY = 128  # Control table address for present velocity
ADDR_PRO_GOAL_CURRENT = 102  # Control table address for goal current
ADDR_PRO_PRESENT_CURRENT = 126  # Control table address for present current
ADDR_PRO_OPERATING_MODE = 11  # Control table address for operating mode

# Control table address for MX model Dynamixel
ADDR_MX_TORQUE_ENABLE = 64  # Control table address for enabling torque
ADDR_MX_GOAL_POSITION = 116  # Control table address for goal position
ADDR_MX_PRESENT_POSITION = 37  # Control table address for present position
ADDR_MX_MOVING_SPEED = 32  # Control table address for moving speed

# Data Byte Length for PRO model Dynamixel
LEN_PRO_GOAL_POSITION = 4  # Data byte length for goal position
LEN_PRO_PRESENT_POSITION = 4  # Data byte length for present position
LEN_PRO_GOAL_VELOCITY = 4  # Data byte length for goal velocity
LEN_PRO_PRESENT_VELOCITY = 4  # Data byte length for present velocity
LEN_PRO_PRESENT_CURRENT = 2  # Data byte length for present current
LEN_PRO_GOAL_CURRENT = 2  # Data byte length for goal current
LEN_PRO_OPERATING_MODE = 1  # Data byte length for operating mode

# Data Byte Length for MX model Dynamixel
LEN_MX_GOAL_POSITION = 2  # Data byte length for goal position
LEN_MX_PRESENT_POSITION = 2  # Data byte length for present position

# Protocol version
PROTOCOL_VERSION = 2.0  # Protocol version used in the Dynamixel

# Default settings
BAUDRATE = 1000000  # Baudrate for communication
DEVICENAME = 'COM3'  # Device name for communication

# Torque control values
TORQUE_ENABLE = 1  # Value for enabling torque
TORQUE_DISABLE = 0  # Value for disabling torque

# Dynamixel position and movement thresholds
DXL_MINIMUM_POSITION_VALUE = 10  # Minimum position value
DXL_MAXIMUM_POSITION_VALUE = 700  # Maximum position value
DXL_MOVING_STATUS_THRESHOLD = 15  # Moving status threshold

# Escape character for loop control
ESC_CHARACTER = 'e'  # Key for escaping loop

# Communication result values
COMM_SUCCESS = 0  # Communication success result value
COMM_TX_FAIL = -1001  # Communication Tx Failed

# Goal and present position and current addresses and lengths
ADDR_GOAL_POSITION = 116  # Goal position address
ADDR_GOAL_CURRENT = 102  # Goal current address
ADDR_PRESENT_POSITION = 132  # Present position address
ADDR_PRESENT_CURRENT = 126  # Present current address

LEN_GOAL_POSITION = 4  # Length of goal position data
LEN_PRESENT_POSITION = 4  # Length of present position data
LEN_GOAL_CURRENT = 2  # Length of goal current data
LEN_PRESENT_CURRENT = 2  # Length of present current data
