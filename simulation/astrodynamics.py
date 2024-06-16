import brahe
import numpy as np

R_EARTH = 6378.0e3  # m

def semi_major_axis(rp, ra):
    """
    rp: periapsis -> radius from the central body to the nearest point on the orbital path
    ra: apoapsis -> radius from the central to the farthest point on the orbital path
    semi major axis: longest semi-diameter of an ellipse.
    """
    return (rp + ra) / 2


def orbital_period(sma, mu):
    """
    sma: semi major axis -> longest semi-diameter of an ellipse.
    mu: standard gravitational parameter of the central body
    """
    return 2.0 * np.pi * np.sqrt((sma**3) / mu)


def eccentricity(rp, ra):
    """
    rp: periapsis -> radius from the central body to the nearest point on the orbital path
    ra: apoapsis -> radius from the central to the farthest point on the orbital path
    """
    semi_major_axis_val = semi_major_axis(rp, ra)
    ecc = 1 - rp / semi_major_axis_val
    return ecc


def get_CART_from_OSC(x_oe, degrees=False):
    """
    Return the cartesian state (position and velocity, ECI) given the corresponding set of osculating orbital elements.
    The vector must contain in order (SatelliteDynamics.jl):
        1. a, Semi-major axis [m]
        2. e, Eccentricity [dimensionless]
        3. i, Inclination [rad]
        4. Ω, Right Ascension of the Ascending Node (RAAN) [rad]
        5. ω, Argument of Perigee [rad]
        6. M, Mean anomaly [rad]
    """
    return np.array(brahe.sOSCtoCART(x_oe, use_degrees=degrees))


def get_OSC_from_CART(x_oe, degrees=False):
    """
    Return the set of osculating orbital elements given the cartesian state (position and velocity, ECI).
    The input vector must be in the following form: [x, y, z, xdot, ydot, zdot]
    The resulting vector will be in order (SatelliteDynamics.jl):
        1. _a_, Semi-major axis [m]
        2. _e_, Eccentricity [dimensionless]
        3. _i_, Inclination [rad]
        4. _Ω_, Right Ascension of the Ascending Node (RAAN) [rad]
        5. _ω_, Argument of Perigee [ramd]
        6. _M_, Mean anomaly [rad]
    """
    return np.array(brahe.sCARTtoOSC(x_oe, use_degrees=degrees))


def axis_angle_to_quaternion(r):
    """
    Converts an axis-angle representation of a rotation to a quaternion.

    Args:
      r: A 3D vector representing the rotation axis and angle.

    Returns:
      A NumPy array representing the quaternion.
    """

    theta = np.linalg.norm(r)
    q = np.array([np.cos(theta / 2), r * np.sinc(theta / (2 * np.pi)) / 2])
    return q
