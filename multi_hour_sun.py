import numpy as np
import matplotlib.pyplot as plt
import data

multi_hour_sun_data = np.load("Data/multi_hour_sun_data.npz")
volts, times = multi_hour_sun_data["volts"], multi_hour_sun_data["unixtime"]
signal_data, v_samp, nsamples = volts, 0.20, len(volts)

multi_hour_sun_signal = data.Signal(signal_data, v_samp, nsamples)
multi_hour_sun_signal.plot_signal("Multi-Hour Sun Data")
plt.show()

multi_hour_sun_signal.plot_power("Multi-Hour Sun Spectra")
plt.show()