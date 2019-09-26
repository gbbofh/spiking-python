class Neuron():
    def __init__(self, scale = 0.02, uSens = 0.2, reset = -65.0, uReset = 2.0):
        """
        Initializes a neuron object

        Parameters:
        (float) scale: The timescale for the recovery variable
        (float) uSens: The sensitivity of the recovery variable
        (float) reset: The post-spike reset value for the membrane potential
        (float) uReset: The post-spike reset value for membrane recovery
        """
        self.scale = scale
        self.uSens = uSens
        self.reset = reset
        self.uReset = uReset

        self.input = 0.0

        self.voltage = self.reset
        self.rec = self.voltage * self.uSens

    def update(self):
        """
        Updates the membrane voltage and recovery variable
        """

        self.voltage += 0.5 * (0.04 * self.voltage ** 2 +
                        5 * self.voltage + 140 - self.rec + self.input)
        self.voltage += 0.5 * (0.04 * self.voltage ** 2 +
                        5 * self.voltage + 140 - self.rec + self.input)
        self.rec += self.scale * (self.uSens * self.voltage - self.rec)

        self.voltage = 30.0 if self.voltage > 30.0 else self.voltage

