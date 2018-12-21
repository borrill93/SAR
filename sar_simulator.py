import numpy as np

class SarSignal:
    def __init__(self, sigma, speed_light, speed_aircraft, bandwidth, frequency,
                 pulsewidth,radar_SRP_range_distance, amplitude):

        '''independent variables'''

        self.sigma = sigma #Radar cross section (RCS), (m**2). 100 is the approximate RCS of a car
        self.speed_light = speed_light #(ms**-1)
        self.speed_aircraft = speed_aircraft #(ms**-1)
        self.bandwidth = bandwidth #Hz
        self.frequency = frequency #Hz
        self.pulsewidth = pulsewidth #s
        self.radar_SRP_range_distance = radar_SRP_range_distance #(m), SRP is the scene reference point
        self.amplitude = amplitude
        self.sampling_rate = self.calculate_sampling_rate()
    '''dependent variables'''

    def calculate_sampling_rate(self):
        '''Calculates the sampling rate'''

        rate = 4/self.frequency
        return rate

    def calculate_chirp_rate(self):
        '''calculates the chirp_rate'''

        rate = self.bandwidth / self.pulsewidth
        return rate

    '''Simulation Geometry initialisation'''

    def target_location_generation(self, number_of_gridpoints=10):
        '''Generates a n by three array, with columns one, two and three
         representing Range (m), Cross-range (m) and RCS (m**2), respectively.'''

        target_location = np.zeros((number_of_gridpoints, 3))
        space_mid_point = int(round(number_of_gridpoints/2))
        target_location[space_mid_point] = np.array([1, 1, self.sigma])
        return target_location

    def get_flight_path(self, images_captured = 10):
        '''Generates an x by y grid representing the flight path of the SAR aircraft.'''

        flight_duration = (10 / self.speed_aircraft * np.size(self.target_location_generation(), 0))
        time = np.linspace(start=0, stop=flight_duration, num=images_captured, endpoint=True)
        flightpath = time * self.speed_aircraft
        return flightpath

    def calculate_radar_SRP_distance(self):
        '''calculates the distance to the SRP from the position of the captured image'''

        flightpath = self.get_flight_path()
        flight_distance = flightpath[-1]
        flight_midpoint = int(flight_distance/2)
        radar_SRP_distance = np.sqrt(self.radar_SRP_range_distance ** 2 +
                                      ((flightpath * -1) + flight_midpoint) ** 2)
        return radar_SRP_distance

    '''Preprocessing'''

    def phase_history(self):
