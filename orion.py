import numpy as np
import matplotlib.pyplot as plt
import data

orion_data = np.load("Data/orion_data.npz")
volts, times = orion_data["voltage"], orion_data["unixtimes"]
signal_data, v_samp, nsamples = volts, 0.20, len(volts)

orion_signal = data.Signal(signal_data, v_samp, nsamples)
#orion_signal.plot_signal("Orion Data")
#plt.show()
#orion_signal.plot_power("Orion Spectra")
#lt.show()