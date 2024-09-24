class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500,
                 set_point=0, limit_output=300):
        """
        初始化PID控制器的参数。
        :param P: 比例系数
        :param I: 积分系数
        :param D: 微分系数
        :param Derivator: 前一次的误差值，用于微分计算
        :param Integrator: 积分值的初始值
        :param Integrator_max: 积分项的最大值
        :param Integrator_min: 积分项的最小值
        :param set_point: 目标设定值
        """
        self.Kp = P  # 比例系数
        self.Ki = I  # 积分系数
        self.Kd = D  # 微分系数
        self.Derivator = Derivator  # 前一次的误差值
        self.Integrator = Integrator  # 积分项
        self.Integrator_max = Integrator_max  # 积分项最大值
        self.Integrator_min = Integrator_min  # 积分项最小值
        self.set_point = set_point  # 目标设定值
        self.limit_output = limit_output  # 输出限制
        self.error = 0.0  # 当前误差

    def calculate(self, current_value):
        """
        计算PID控制器输出。
        :param current_value: 当前值
        :return: PID控制器的输出
        """
        # 计算误差 = 目标值 - 当前值
        self.error = self.set_point - current_value

        # 比例项计算
        self.P_value = self.Kp * self.error

        # 微分项计算，使用当前误差与前一次误差的差值
        self.D_value = self.Kd * (self.error - self.Derivator)
        self.Derivator = self.error  # 保存当前误差，供下次计算使用

        # 积分项累加当前误差
        self.Integrator += self.error
        # 限制积分项的累加范围，防止积分饱和
        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        # 积分项计算
        self.I_value = self.Integrator * self.Ki

        # PID总和
        PID_output = self.P_value + self.I_value + self.D_value

        # 限制PID输出的范围，防止超调或欠调
        if PID_output > self.limit_output:
            PID_output = self.limit_output
        elif PID_output < -self.limit_output:
            PID_output = -self.limit_output

        return PID_output
