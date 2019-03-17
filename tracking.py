import numpy as np
import ugradio
import tool_box as tb
import time

DT = 5  # timestep for tracking
tolerance = 1  # pointing tolerance in degrees
max_time = tb.time["Julian"]() + 3600  # when to stop pointing

def difference(a, b):
    return np.abs(a - b)


def west_coordinates(pointing_coordinates):
    return pointing_coordinates['ant_w']


def east_coordinates(pointing_coordinates):
    return pointing_coordinates['ant_e']


def print_pointing_coordinates(w_altitude, w_azimuth, e_altitude, e_azimuth):
    print('west pointed:' + str(w_altitude) + ',' + str(w_azimuth))
    print('east pointed:' + str(e_altitude) + ',' + str(e_azimuth) + '\n')


def over_tolerance(altitude, azimuth, w_altitude, w_azimuth, e_altitude, e_azimuth):
    return (difference(altitude, e_altitude) > tolerance or
            difference(azimuth, e_azimuth) > tolerance or
            difference(altitude, w_altitude) > tolerance or
            difference(azimuth, w_azimuth) > tolerance)


def track_object(altitude, azimuth, position_calculator):
    ifm = ugradio.interf.Interferometer()
    print('pointing dishes')
    ifm.point(altitude, azimuth)
    print('first pointing done')
    try:
        while True:
            if tb.time["Julian"]() > max_time:
                print('observing successful')
                break
            altitude, azimuth = position_calculator()  # recompute position
            ifm.point(altitude, azimuth)
            pointing_coordinates = ifm.get_pointing()
            w_altitude, w_azimuth = west_coordinates(pointing_coordinates)
            e_altitude, e_azimuth = east_coordinates(pointing_coordinates)

            print('target:' + str(altitude) + ',' + str(azimuth))
            print_pointing_coordinates(w_altitude, w_azimuth, e_altitude, e_azimuth)

            if over_tolerance(altitude, azimuth, w_altitude, w_azimuth, e_altitude, e_azimuth):
                raise Exception('bad pointing')
            time.sleep(DT)
    except Exception as e:
        print(e)
    finally:
        ifm.stow()

