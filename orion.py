import numpy as np
import rotation as rot
import matplotlib.pyplot as plt
import data
import least_squares_fitting as lsf


galactic_coordinates = (209.0137, -19.3816)
ra, dec = rot.rotate(galactic_coordinates, rot.GAL_to_EQ_rotation())

orion_data = np.load("Data/orion_data.npz")
volts, times = orion_data["voltage"], orion_data["unixtimes"]
polyfit = np.polyfit(times, volts, deg=2)
orion_fit = np.polyval(polyfit, times)
volts = volts - orion_fit
v_samp, nsamples = 0.20, len(volts)
lsf.get_baseline_script(ra, dec, volts, times)

#orion_signal = data.Signal(signal_data, v_samp, nsamples)

#orion_signal.plot_signal("Orion Data")
#plt.show()
#orion_signal.plot_power("Orion Spectra")
#plt.show()