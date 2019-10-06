import numpy
import scipy.stats as stats

#TODO:
# If the number of neurons being simulated is particularly large
# (~10,000, maybe less), the model becomes unstable
# I don't know if this is a quirk that is handled
# behind the scenes by matlab, because I don't really use
# matlab at all...
# I could provide a hard-coded bound for the input, but I'm
# Not sure if this is a good idea, or not.
class Network():
    """
    Implements the simple spiking model by Eugene Izhikevich

    Generates a randomly connected network of numEx + numIn neurons with
    random properties, as described in the paper
    'A Simple Model of Spiking Neurons' (2003).
    """
    def __init__(self, numEx, numIn):
        """
        Constructs a randomly connected spiking neural network

        Parameters:
        numEx (int): The number of excitatory neurons to generate
        numIn (int): The number of inhibitory neurons to generate
        """

        self.numEx = numEx
        self.numIn = numIn
        totalNum = numEx + numIn

        self.pSpikes = numpy.zeros((totalNum, 1))

        r = stats.uniform.rvs(size=(totalNum))

        self.scale = numpy.ones(totalNum)
        self.uSens = numpy.ones(totalNum)
        self.reset = numpy.ones(totalNum)
        self.uReset = numpy.ones(totalNum)

        self.scale[0 : numEx] *= 0.02
        self.scale[numEx : ] *= 0.02 + 0.08 * r[numEx : ]
        self.uSens[0 : numEx] *= 0.2
        self.uSens[numEx : ] *= 0.25 - 0.05 * r[numEx : ]
        self.reset[0 : numEx] *= -65 + 15 * r[0 : numEx] ** 2
        self.reset[numEx : ] *= -65
        self.uReset[0 : numEx] *= 8 - 6 * r[0 : numEx] ** 2
        self.uReset[numEx : ] *= 2

        # The original code which used list comprehension
        # took an obscene amount of time to do this...
        # This runs absurdly fast in comparison.
        self.synapses = numpy.ones((totalNum, totalNum))
        self.synapses[0 : numEx] *= 0.5 * stats.uniform.rvs(size=totalNum)
        self.synapses[numEx : ] *= -stats.uniform.rvs(size=totalNum)

        self.voltage = numpy.full(totalNum, -65.0)
        self.recovery = numpy.multiply(self.voltage, self.uSens)
        self.input = numpy.zeros(totalNum)


    def update(self):
        """
        Updates the membrane potential for all neurons in the network

        Returns:
        list: The list of spikes which were generated in the previous timestep
        """

        spikes = numpy.where(self.voltage >= 30.0)[0]
        self.input += self.synapses[spikes, :].sum(axis=0)

        self.voltage[spikes] = self.reset[spikes]
        self.recovery[spikes] += self.uReset[spikes]

        self.voltage += 0.5 * (0.04 * self.voltage ** 2 +
                       5.0 * self.voltage + 140 - self.recovery + self.input)
        self.voltage += 0.5 * (0.04 * self.voltage ** 2 +
                       5.0 * self.voltage + 140 - self.recovery + self.input)
        self.recovery += self.scale * (self.voltage * self.uSens - self.recovery)

        self.voltage[numpy.where(self.voltage >= 30.0)] = 30.0

        self.pSpikes = spikes
        return spikes
