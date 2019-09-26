class Neuron():
    def __init__(self, scale = 0.02, uSens = 0.2, reset = -65.0, uReset = 2.0):
        self.scale = scale
        self.uSens = uSens
        self.reset = reset
        self.uReset = uReset

        self.input = 0.0

        self.voltage = self.reset
        self.rec = self.voltage * self.uSens

    def update(self):

        self.voltage += 0.5 * (0.04 * self.voltage ** 2 +
                        5 * self.voltage + 140 - self.rec + self.input)
        self.voltage += 0.5 * (0.04 * self.voltage ** 2 +
                        5 * self.voltage + 140 - self.rec + self.input)
        self.rec += self.scale * (self.uSens * self.voltage - self.rec)

        self.voltage = 30.0 if self.voltage > 30.0 else self.voltage

