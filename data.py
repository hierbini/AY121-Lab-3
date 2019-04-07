import numpy as np
import matplotlib.pyplot as plt
import tool_box as tb
import plot


class Signal:

    def __init__(self, signal, v_samp, nsamples):
        self.signal = signal
        self.v_samp = v_samp
        self.nsamples = nsamples
        self.freq, self.power = self.get_power()

    def plot_signal(self, title="Insert Title"):
        self.signal_plot = plt.figure(figsize=[15, 6])
        plot.plot_signal(self.signal, self.nsamples, self.v_samp, title=title)

    def get_power(self):
        """
        Returns the power spectrum of a given signal as a function of frequency

        Parameters:
        signal (array) : signal data
        v_samp (double) : sampling frequency
        nsamples (int) : number of samples per block

        Returns:
        power (array) : power spectrum
        freqs (array) : frequencies
        """
        fourier_transform = tb.fft(self.signal)
        power = np.abs(fourier_transform) ** 2
        dt = 1 / self.v_samp
        freqs = tb.freq(power.size, d=dt)
        return freqs, power

    def plot_power(self, title="Insert Title"):
        self.power_plot = plt.figure(figsize = [15, 6])
        plot.plot_power(self.power, self.freq, title=title)