import numpy as np
import matplotlib.pyplot as plt
import data

sun_data = np.load("Data/one_hour_sun_data.npz")
volts, times = sun_data["volts"], sun_data["unixtime"]
signal_data, v_samp, nsamples = volts, 0.20, len(volts)

sun_signal = data.Signal(signal_data, v_samp, nsamples)
sun_signal.plot_signal("Sun Data")
plt.show()

sun_signal.plot_power("Sun Spectra")
plt.show()