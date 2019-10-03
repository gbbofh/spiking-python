import network

import datetime
import scipy.stats as stat
import matplotlib.pyplot as plot

def main():
    k = 100
    time_max = 1000

    spikes = []
    times = []

    t0 = datetime.datetime.now()
    net = network.Network(7 * k, 3 * k)
    t1 = datetime.datetime.now()

    fig = plot.figure(figsize=(6,6))

    print('configured network in:', t1 - t0)

    t0 = datetime.datetime.now()

    for t in range(time_max):
        for neuron in net.get_excitatory():
            neuron.input = 5.0 * stat.norm.rvs(size=1)[0]

        for neuron in net.get_inhibitory():
            neuron.input = 2.0 * stat.norm.rvs(size=1)[0]

        tmp = net.update()
        spikes += tmp
        for n in tmp:
            times.append(t)

    t1 = datetime.datetime.now()

    print('simulated', time_max, 'steps in: ', t1 - t0)

    ax1 = fig.add_subplot(111)
    ax1.plot(times, spikes, ',k')

    xl, xr = ax1.get_xlim()
    yb, yt = ax1.get_ylim()

    ax1.set_aspect(abs((xr - xl) / (yb - yt))  * 1.0)
    ax1.axhline(color='r', y=net.numEx - 0.5, xmax=time_max)

    plot.show()

if __name__ == "__main__":
    main()
