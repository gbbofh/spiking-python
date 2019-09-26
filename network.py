import neuron
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
        self.neurons = []
        self.synapses = []
        self.numEx = numEx
        self.numIn = numIn
        self.pSpikes = []

        totalNum = numEx + numIn

        r = stats.uniform.rvs(size=(totalNum))


        # Not the best way to do it -- but I set out with
        # an object oriented design in mind -- this still happens to
        # work way faster than the code that is commented out down
        # below.
        scale = [0.02 if i < numEx else 0.02 + 0.08 * r[i]
                 for i in range(totalNum)]
        uSens = [0.2 if i < numEx else 0.25 - 0.05 * r[i]
                 for i in range(totalNum)]
        reset = [-65.0 + 15 * r[i] ** 2 if i < numEx else -65.0
                 for i in range(totalNum)]
        uReset = [6 - 6 * r[i] ** 2 if i < numEx else 2.0
                 for i in range(totalNum)]

        self.neurons = [neuron.Neuron(scale[i], uSens[i], reset[i], uReset[i])
                        for i in range(totalNum)]

        self.synapses = [[0.5 * stats.uniform.rvs() for i in range(totalNum)]
                         if j < numEx else
                         [-stats.uniform.rvs() for i in range(totalNum)]
                         for j in range(totalNum)]

        # Old code from initial prototyping -- here for posterity
        #for i in range(numEx):
        #    self.neurons.append(neuron.Neuron(0.02, 0.2,
        #                                  -65 + 15 * r[i] ** 2,
        #                                  8 - 6 * r[i] ** 2))
        #    self.synapses.append([])
        #    for i in range(numEx + numIn):
        #        self.synapses[-1].append(0.5 * stats.uniform.rvs(size=1)[0])

        #    self.neurons[-1].voltage = -65

        #for i in range(numIn):
        #    self.neurons.append(neuron.Neuron(0.02 + 0.08 * r[numEx + i],
        #                                  0.25 - 0.05 * r[numEx + i], -65, 2))
        #    self.synapses.append([])
        #    for i in range(numEx + numIn):
        #        self.synapses[-1].append(-stats.uniform.rvs(size=1)[0])

        #    self.neurons[-1].voltage = -65
        #    self.neurons[-1].rec = (self.neurons[-1].uSens *
        #                           self.neurons[-1].voltage)


    # This can't really be optimized easily. If I flatten everything out
    # into lists and keep them as members of Network, then I can use list
    # comprehensions to update all of the values. This gave a speedboost of
    # about 2x when I made the change in __init__
    # but updating the values here isn't so simple...
    # This is probably one of those situations where it would be more
    # beneficial speed-wise to take a data-oriented design approach,
    # rather than an object oriented design approach.
    def update(self):
        """
        Updates the membrane potential for all neurons in the network

        Returns:
        list: The list of spikes which were generated in the previous timestep
        """

        # Dead code, for now.
        spikes = [i for i,n in enumerate(self.neurons) if n.voltage >= 30.0]

        # spikes = []

        for i in spikes:
            n = self.neurons[i]
            n.voltage = n.reset
            n.rec = n.rec + n.uReset
            for j,_ in enumerate(self.synapses[i]):
                self.neurons[j].input += self.synapses[i][j]

        # This code originally did the job of the above
        # for loop and list comprehension
        # It is here for posterity.
        # for i,neuron in enumerate(self.neurons):

        #     if neuron.voltage >= 30.0:
        #         spikes.append(i)
        #         neuron.voltage = neuron.reset
        #         neuron.rec = neuron.rec + neuron.uReset

        #         for j,_ in enumerate(self.synapses[i]):
        #             self.neurons[j].input += self.synapses[i][j]

        for neuron in self.neurons:
            neuron.update()

        self.pSpikes = spikes
        return spikes

    def get_excitatory(self):
        """
        Retrieves only the excitatory neurons

        Returns:
        list: A list containing only the excitatory neurons
        """
        return self.neurons[0 : self.numEx]

    def get_inhibitory(self):
        """
        Retrieves only the inhibitory neurons

        Returns:
        list: A list containing only the inhibitory neurons
        """
        return self.neurons[self.numEx : self.numEx + self.numIn]
