import numpy
import scipy.stats as stats

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


        # This init code still runs very slowly. Eventually I will update it to
        # take advantage of numpy's broadcasting, as opposed to constructing
        # a list and converting it to a numpy array afterwards. But I am
        # currently focused on getting this thing to work at all.
        self.scale = numpy.array([0.02 if i < numEx else 0.02 + 0.08 * r[i]
                 for i in range(totalNum)])
        self.uSens = numpy.array([0.2 if i < numEx else 0.25 - 0.05 * r[i]
                 for i in range(totalNum)])
        self.reset = numpy.array([-65.0 + 15 * r[i] ** 2 if i < numEx else -65.0
                 for i in range(totalNum)])
        self.uReset = numpy.array([6 - 6 * r[i] ** 2 if i < numEx else 2.0
                 for i in range(totalNum)])

        self.synapses = numpy.array([[0.5 * stats.uniform.rvs()
                                    for i in range(totalNum)]
                                     if j < numEx else
                                     [-stats.uniform.rvs()
                                      for i in range(totalNum)]
                                     for j in range(totalNum)])
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
        #self.input += numpy.where(self.voltage >= 30, 1, 0).dot(self.synapses)
        #self.input[spikes] += self.synapses.transpose()[spikes].dot(spikeVec)
        #self.input[spikes] += self.synapses.transpose()[spikes] * spikeVec
        #if len(spikes) > 0:
            #self.input += (self.synapses.transpose()[:,spikes].transpose() * spikeVec)[0]
            #self.input += numpy.sum((self.synapses[:,spikes] * spikeVec).transpose(), axis=0)
        #self.input += self.synapses[:,spikes].sum(axis=1)
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
