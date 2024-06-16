import brahe
import numpy as np

from astrodynamics import R_EARTH
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



class SunVector:
    def __init__(self, noise_std_deg, rotation_offset_deg, lux_max_range=144000):
        self.noise_std = np.deg2rad(noise_std_deg)
        self.offset = np.deg2rad(rotation_offset_deg)
        self.lux_max_range = lux_max_range

    def sun_vector_body_frame(self, spacecraft):
        r_sun_eci = brahe.sun_position(spacecraft.epoch)
        # Vector from the spacecraft to the Sun in ECI frame
        vec_sun_eci = r_sun_eci - spacecraft.orbit_eci[:3]
        # Vector from the spacecraft to the Sun in body frame
        return dcm_from_q(spacecraft.attitude) @ (vec_sun_eci / np.linalg.norm(vec_sun_eci))  # normalized

    def measure(self, spacecraft):
        if self.eclipse_state(spacecraft):
            return np.zeros(3)
        else:
            vec_sun_body = self.sun_vector_body_frame(spacecraft)
            return apply_SO3_noise(vec_sun_body, self.noise_std)


    def measure_lux(self, spacecraft):

        if self.eclipse_state(spacecraft):
            return np.zeros(spacecraft.surface_normals.shape[0])
        else:
            # no eclipse
            vec_sun_body = self.sun_vector_body_frame(spacecraft)
            normals = spacecraft.surface_normals
            lux = np.dot(normals, vec_sun_body)
            # Negative ones means no field of view of the sun, so 0 lux
            lux[lux < 0.0] = 0.0
            return lux
            
    def eclipse_state(self, spacecraft):
        """ 
        Computes the illumination fraction of a satellite in Earth orbit using a cylindrical Earth shadow model. 
        O. Montenbruck, and E. Gill, Satellite Orbits: Models, Methods and Applications_, 2012, p.80-83.                         
        """
        r_sun_eci = brahe.sun_position(spacecraft.epoch)
        r_sun_eci_normalized = r_sun_eci / np.linalg.norm(r_sun_eci)
        # Projection of spacecraft position
        s_proj = np.dot(spacecraft.orbit_eci[:3], r_sun_eci_normalized) 

        # Illumination fraction (0 <= nu <= 1). nu = 0 means
        # spacecraft in complete shadow, nu = 1 mean spacecraft
        # fully illuminated by sun.
        nu = True
        if s_proj/np.linalg.norm(s_proj) >= 1.0 or np.linalg.norm(spacecraft.orbit_eci[:3] - s_proj*r_sun_eci_normalized) > R_EARTH:
            nu = False
        return nu

  

class LightSensor:
    def __init__(self, noise_std_deg, rotation_offset_deg):
        self.noise_std = np.deg2rad(noise_std_deg)
        self.offset = np.deg2rad(rotation_offset_deg)

    def measure(self, spacecraft):
        pass


class Accelerometer:
    # Not useful given our lack of propulsion but migth be helpful for ground testing / debugging
    def __init__():
        pass

    def measure(self, spacecraft):
        pass

class GPS:
    def __init__(self, std):
        self.std = std

    def measure(self, spacecraft):
        pass


# TODO other sensors
