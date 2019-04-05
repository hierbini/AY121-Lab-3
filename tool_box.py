from __future__ import print_function
import numpy as np
import ugradio


units = {"time": "($\mu$s)",
         "frequency": "(Hz)",
         "temperature": "(K)",
         "velocity": "($km \cdot s^{-1}$)",
         "voltage": "($\mu$V)",
         "voltage spectra": "($\mu V \cdot \mu s$)",
         "power spectra": "($\mu V^{2} \cdot \mu s^{2}$)"
        }


time = {"Local": ugradio.timing.local_time,
        "UTC": ugradio.timing.utc, # current UTC as a string
        "UTC seconds": ugradio.timing.unix_time,
        "Julian": ugradio.timing.julian_date, # current Julian day and time,
        "LST": ugradio.timing.lst # current LST at NCH
       }


fft = np.fft.fft
shift = np.fft.fftshift
freq = np.fft.fftfreq

def RA_and_DEC_from_unixtimes(unixtimes, source="sun"):
    """
    Returns right ascension and declination from an array of unixtimes 
    (only relevant for objects within the solar system, i.e. sun and moon)

    Parameters:
    unixtimes (int array): unixtimes from interferometer data
    source (string): indicate "sun" or "moon"

    Returns:
    ra (float array): right ascension in radians
    dec (float array): declination in radians
    """
    julian_dates = time["Julian"](unixtimes)
    print(julian_dates)

    if source == "sun":
        position = [ugradio.coord.sunpos(jd) for jd in julian_dates]
    if source == "moon":
        position = [ugradio.coord.moonpos(jd) for jd in julian_dates]

    ra = np.array([position[jd][0] for jd in range(len(julian_dates))])
    dec = np.array([position[jd][1] for jd in range(len(julian_dates))])
    return np.radians(ra), np.radians(dec)


def LST_from_unixtimes(unixtimes):
    """
    Returns local sidereal times from array of unixtimes
    
    Parameters:
    unixtimes (int array): unixtimes from interferometer data

    Returns:
    lst (float array): Returns local sidereal time in radians
    """
    julian_dates = time["Julian"](unixtimes)
    lst = time["LST"](julian_dates)
    return lst


def hour_angle(lst, ra):
    """
    Calculates the hour angle given local sidereal time and right ascension

    Parameters:
    lst (float array): local sidereal time in radians
    ra (float array): right ascension in radians

    Returns:
    hour angles (float array): equal to (lst - ra)
    """
    return lst - ra


def save_picture(fig, title):
    fig.savefig("Pictures\\" + title + '.png')
