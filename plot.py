import matplotlib.pyplot as plt
import tool_box as tb
import numpy as np


def plot_signal(signal, nsamples, v_samp, title="Insert Title"):
    N = nsamples
    time = np.linspace(-N / (2.0 * v_samp), N / (2.0 * v_samp), num=N, endpoint=False)
    plt.plot(time, signal, color="c", linewidth=1.0)
    plt.ylabel("Voltage")
    plt.xlabel("Time")
    plt.title(title)
    plt.grid()


def plot_power(power, frequencies, title="Insert Title"):
    plt.plot(tb.shift(frequencies), tb.shift(power), color="c", linewidth=1.0)
    plt.ylabel("Power")
    plt.xlabel("Frequency")
    plt.title(title)
    plt.grid()