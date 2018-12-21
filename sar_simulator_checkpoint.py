import numpy as np

'''independent variables'''
sigma = 100  #Radar cross section (RCS), (m**2). 100 is the approximate RCS of a car
speed_light = 299792458 #(ms**-1)
speed_aircraft = 250 #(ms**-1)
bandwidth = 4e5 #Hz
frequency = 5e6 #Hz
pulsewidth = 1e-06 #s
radar_SRP_range_distance = 100 #(m), SRP is the scene reference point
amplitude = 10

'''dependent variables'''
sampling_rate = 4/frequency #frequency
chirp_rate = bandwidth/pulsewidth

string_str()

def target_location_generation(number_of_gridpoints=10, ):
    '''Generates a n by three array, with columns one, two and three
     representing Range (m), Cross-range (m) and RCS (m**2), respectively.'''

    target_location = np.zeros((number_of_gridpoints, 3))
    space_mid_point = int(round(number_of_gridpoints/2))
    target_location[space_mid_point] = np.array([1, 1, sigma])
    return target_location

def flight_path_generation(images_captured = 10):
    '''Generates an x by y grid representing the flight path of the SAR aircraft.'''

    flight_duration = (10 / speed_aircraft * np.size(target_location_generation(), 0))
    time = np.linspace(start=0, stop=flight_duration, num=images_captured, endpoint=True)
    flightpath = time * speed_aircraft
    return flightpath

def radar_SRP_distance_calculator():
    '''calculates the distance to the SRP from the position of the captured image'''

    flight_distance = flight_path_generation()[-1]
    flight_midpoint = int(flight_distance/2)
    flightpath = np.array(flight_path_generation())
    radar_SRP_distance_squared = (radar_SRP_range_distance ** 2 +
                                  (flight_midpoint - flightpath) ** 2)
    radar_SRP_distance = np.sqrt(radar_SRP_distance_squared)
    return radar_SRP_distance



#position_distance = np.stack((flight_path_generation(),radar_SRP_distance_calculator()), axis=-1)


