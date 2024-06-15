import brahe
import numpy as np

from magnetic import get_magnetic_field_ECI
from transformations import dcm_from_phi, dcm_from_q


def apply_SO3_noise(vec, std):
    """
    Adds S03-style noise to a vector by rotating it about a random axis.

    Args:
        vec: The vector to which noise will be added.
        std: The standard deviation of the noise.

    Returns:
        The noisy vector.
    """
    noise = std * np.random.randn(3)
    return dcm_from_phi(noise) @ vec


class Magnetometer:
    def __init__(self, noise_std_deg, offset=None):
        self.std_noise = np.deg2rad(noise_std_deg)
        if offset == None:
            self.offset = dcm_from_phi(self.std_noise*np.random.randn(3))
        else:
            self.offset = offset

    def measure(self, spacecraft):
        B_ECI = get_magnetic_field_ECI(spacecraft.epoch, spacecraft.orbit_eci)
        B_body = dcm_from_q(spacecraft.attitude) @ B_ECI
        return apply_SO3_noise(self.offset @ B_body, self.std_noise) 
    


class Gyroscope:
    def __init__(self, rotate_std_deg, noise_std_deg, initial_bias_deg, bias_std_noise=1e-3):
        self.offset = dcm_from_phi(np.deg2rad(rotate_std_deg) * np.random.randn(3))
        self.std_noise = np.deg2rad(noise_std_deg) 

        randvec = np.random.randn(3)
        self.bias = np.deg2rad(initial_bias_deg) * randvec / np.linalg.norm(randvec) # TODO bias dynamics
        self.bias_std_noise = bias_std_noise

    def measure(self, spacecraft):
        measurement = self.offset @ spacecraft.angular_velocity + self.std_noise * np.random.randn(3) + self.bias + self.bias_std_noise * np.random.randn(3)
        return measurement


class Accelerometer:
    # Not useful given our lack of propulsion but migth be helpful for ground testing / debugging

    def __init__():
        pass

    def measure(self, spacecraft):
        pass

class SunSensor:
    def __init__(self, std_deg, offset=None):
        self.std = np.deg2rad(std_deg)
        self.offset = offset

    def measure(self, spacecraft):
        r_sun = brahe.sun_position(spacecraft.epoch)
        vec_sun_body = self.get_sun_vec_body(spacecraft.orbit_eci, r_sun, spacecraft.attitude)
        return apply_SO3_noise(vec_sun_body, self.std)

    def get_sun_vec_body(self, x_eci, sun_eci, attitude_q):
        # Vector from the spacecraft to the Sun in ECI frame
        vec_sun_eci = sun_eci - x_eci
        # Vector from the spacecraft to the Sun in body frame
        vec_sun_body = dcm_from_q(attitude_q) @ (vec_sun_eci / np.linalg.norm(vec_sun_eci))  # normalized
        return vec_sun_body

    # TODO Flux values


class GPS:
    def __init__(self, std):
        self.std = std

    def measure(self, spacecraft):
        pass


# TODO other sensors
