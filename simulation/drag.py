"""
Directlt translated into python from https://github.com/sisl/SatelliteDynamics.jl/blob/master/src/orbit_dynamics.jl

References:
1. O. Montenbruck, and E. Gill, _Satellite Orbits: Models, Methods and Applications_, 2012, p.89-91.


"""

import brahe
import numpy as np
import pandas as pd
from brahe import coordinates
from nrlmsise00 import msise_flat

OMEGA_EARTH = 7.292115146706979e-5  # [rad/s] (Vallado 4th Ed page 222)


def density_harris_priester(x, r_sun):
    # Harris-Priester Constants
    hp_upper_limit = 1000.0  # Upper height limit [km]
    hp_lower_limit = 100.0  # Lower height limit [km]
    hp_ra_lag = 0.523599  # Right ascension lag [rad]
    hp_n_prm = 3  # Harris-Priester parameter
    hp_N = 50  # Number of coefficients

    # Height [km]
    hp_h = np.array(
        [
            100.0,
            120.0,
            130.0,
            140.0,
            150.0,
            160.0,
            170.0,
            180.0,
            190.0,
            200.0,
            210.0,
            220.0,
            230.0,
            240.0,
            250.0,
            260.0,
            270.0,
            280.0,
            290.0,
            300.0,
            320.0,
            340.0,
            360.0,
            380.0,
            400.0,
            420.0,
            440.0,
            460.0,
            480.0,
            500.0,
            520.0,
            540.0,
            560.0,
            580.0,
            600.0,
            620.0,
            640.0,
            660.0,
            680.0,
            700.0,
            720.0,
            740.0,
            760.0,
            780.0,
            800.0,
            840.0,
            880.0,
            920.0,
            960.0,
            1000.0,
        ]
    )

    # Minimum density [g/km^3]
    hp_c_min = np.array(
        [
            4.974e05,
            2.490e04,
            8.377e03,
            3.899e03,
            2.122e03,
            1.263e03,
            8.008e02,
            5.283e02,
            3.617e02,
            2.557e02,
            1.839e02,
            1.341e02,
            9.949e01,
            7.488e01,
            5.709e01,
            4.403e01,
            3.430e01,
            2.697e01,
            2.139e01,
            1.708e01,
            1.099e01,
            7.214e00,
            4.824e00,
            3.274e00,
            2.249e00,
            1.558e00,
            1.091e00,
            7.701e-01,
            5.474e-01,
            3.916e-01,
            2.819e-01,
            2.042e-01,
            1.488e-01,
            1.092e-01,
            8.070e-02,
            6.012e-02,
            4.519e-02,
            3.430e-02,
            2.632e-02,
            2.043e-02,
            1.607e-02,
            1.281e-02,
            1.036e-02,
            8.496e-03,
            7.069e-03,
            4.680e-03,
            3.200e-03,
            2.210e-03,
            1.560e-03,
            1.150e-03,
        ]
    )

    # Maximum density [g/km^3]
    hp_c_max = np.array(
        [
            4.974e05,
            2.490e04,
            8.710e03,
            4.059e03,
            2.215e03,
            1.344e03,
            8.758e02,
            6.010e02,
            4.297e02,
            3.162e02,
            2.396e02,
            1.853e02,
            1.455e02,
            1.157e02,
            9.308e01,
            7.555e01,
            6.182e01,
            5.095e01,
            4.226e01,
            3.526e01,
            2.511e01,
            1.819e01,
            1.337e01,
            9.955e00,
            7.492e00,
            5.684e00,
            4.355e00,
            3.362e00,
            2.612e00,
            2.042e00,
            1.605e00,
            1.267e00,
            1.005e00,
            7.997e-01,
            6.390e-01,
            5.123e-01,
            4.121e-01,
            3.325e-01,
            2.691e-01,
            2.185e-01,
            1.779e-01,
            1.452e-01,
            1.190e-01,
            9.776e-02,
            8.059e-02,
            5.741e-02,
            4.210e-02,
            3.130e-02,
            2.360e-02,
            1.810e-02,
        ]
    )

    # Satellite height
    # geod = brahe.sECEFtoGEOD(x[0:3], use_degrees=True)
    height = x[2] / 1000.0  # height in [km]

    # Exit with zero density outside height model limits
    if height > hp_upper_limit or height < hp_lower_limit:
        return 0.0

    # Sun right ascension, declination
    ra_sun = np.arctan2(r_sun[1], r_sun[0])
    dec_sun = np.arctan2(r_sun[2], np.sqrt(r_sun[0] ** 2 + r_sun[1] ** 2))

    # Unit vector u towards the apex of the diurnal bulge
    # in inertial geocentric coordinates
    c_dec = np.cos(dec_sun)
    u = np.array(
        [
            c_dec * np.cos(ra_sun + hp_ra_lag),
            c_dec * np.sin(ra_sun + hp_ra_lag),
            np.sin(dec_sun),
        ]
    )

    # Cosine of half angle between satellite position vector and
    # apex of diurnal bulge
    c_psi2 = 0.5 + 0.5 * np.dot(x, u) / np.linalg.norm(x)

    # Height index search and exponential density interpolation
    ih = 0  # section index reset
    for i in range(hp_N):
        if height >= hp_h[i] and height < hp_h[i + 1]:
            ih = i  # ih identifies height section
            break

    h_min = (hp_h[ih] - hp_h[ih + 1]) / np.log(hp_c_min[ih + 1] / hp_c_min[ih])
    h_max = (hp_h[ih] - hp_h[ih + 1]) / np.log(hp_c_max[ih + 1] / hp_c_max[ih])

    d_min = hp_c_min[ih] * np.exp((hp_h[ih] - height) / h_min)
    d_max = hp_c_max[ih] * np.exp((hp_h[ih] - height) / h_max)

    # Density computation
    density = d_min + (d_max - d_min) * c_psi2**hp_n_prm

    # Convert from g/km^3 to kg/m^3
    density *= 1.0e-12

    return density


def retrieve_sw_data(epoch_dt, sw):
    # Load space weather data
    # sw = sw_daily()

    # Check and set the timezone to UTC if it's not already
    if sw.index.tz is None:
        sw = sw.tz_localize("utc")

    epoch = pd.to_datetime(epoch_dt, utc=True)

    # Calculate the previous day for f10.7
    epoch_prev = epoch - pd.to_timedelta("1d")

    # Retrieve the specific data
    ap = sw.at[epoch.floor("D"), "Apavg"]
    f107 = sw.at[epoch_prev.floor("D"), "f107_obs"]
    f107a = sw.at[epoch.floor("D"), "f107_81ctr_obs"]

    return ap, f107, f107a


def compute_rho(epoch_dt, altitude, latitude, longitude, sw):
    ap, f107, f107a = retrieve_sw_data(epoch_dt, sw)
    rho = msise_flat(epoch_dt, altitude, latitude, longitude, f107a, f107, ap, method="gt7d")[5]
    rho = rho * 1000
    return rho


def accel_drag(epoch_dt, x, mass, area, Cd, T, sw):
    """
    Computes the perturbing, non-conservative acceleration caused by atmospheric
    drag assuming that the ballistic properties of the spacecraft are captured by
    the coefficient of drag.

    Arguments:
    - `x`: Satellite Cartesean state in the ECI frame [m; m/s]
    - `rho`: atmospheric density [kg/m^3]
    - `mass`: Spacecraft mass [kg]
    - `area`: Wind-facing cross-sectional area [m^2]
    - `Cd`: coefficient of drag [dimensionless]
    - `T`: Rotation matrix from the inertial to the true-of-date frame
    """
    # Constants
    omega = np.array([0, 0, OMEGA_EARTH])  # You need to define OMEGA_EARTH with the appropriate value

    # Position and velocity in true-of-date system
    r_tod = np.dot(T, x[:3])
    v_tod = np.dot(T, x[3:6])

    # Velocity relative to the Earth's atmosphere
    v_rel = v_tod - np.cross(omega, r_tod)
    v_abs = np.linalg.norm(v_rel)

    r_eci = x[0:3]
    r_ecef = T @ r_eci

    longitude, latitude, altitude = coordinates.sECEFtoGEOC(r_ecef, use_degrees="true")

    rho = compute_rho(epoch_dt, altitude / 1000, latitude, longitude, sw)
    # print('rho', rho)

    # Acceleration
    a_tod = -0.5 * Cd * (area / mass) * rho * v_abs * v_rel
    a_drag = np.dot(T.T, a_tod)

    return a_drag
