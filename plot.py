import matplotlib.pyplot as plt
import tool_box as tb
import numpy as np


def plot_signal(signal, nsamples, v_samp, title="Insert Title"):
    N = nsamples
    time = np.linspace(-N / (2.0 * v_samp), N / (2.0 * v_samp), num=N, endpoint=False)
    plt.plot(time, signal, color="k")
    plt.ylabel("Voltage " + tb.units["voltage"])
    plt.xlabel("Time" + tb.units["time"])
    plt.title(title)


def plot_power(power, frequencies, title="Insert Title"):
    plt.plot(tb.shift(frequencies), tb.shift(power), color="k")
    plt.ylabel("Power " + tb.units["power spectra"])
    plt.xlabel("Frequency" + tb.units["frequency"])
    plt.title(title)