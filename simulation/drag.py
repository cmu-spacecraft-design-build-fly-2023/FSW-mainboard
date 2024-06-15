"""
Directlt translated into python from https://github.com/sisl/SatelliteDynamics.jl/blob/master/src/orbit_dynamics.jl

References:
1. O. Montenbruck, and E. Gill, _Satellite Orbits: Models, Methods and Applications_, 2012, p.89-91.


"""

import numpy as np
import pandas as pd
from brahe import coordinates
import spaceweather
from nrlmsise00 import msise_flat

OMEGA_EARTH = 7.292115146706979e-5  # [rad/s] (Vallado 4th Ed page 222)


_SW = None

def initialize_spaceweather():
    global _SW
    _SW = spaceweather.sw_daily(update=True)
    # Check and set the timezone to UTC if it's not already
    if _SW.index.tz is None:
        _SW = _SW.tz_localize("utc")

initialize_spaceweather()


def compute_density_nrlmsise00(epoch_dt, altitude, latitude, longitude): 

    epoch = pd.to_datetime(epoch_dt, utc=True)

    # Calculate the previous day for f10.7
    epoch_prev = epoch - pd.to_timedelta("1d")

    # Retrieve the specific data
    ap =  _SW.at[epoch.floor("D"), "Apavg"]
    f107 =  _SW.at[epoch_prev.floor("D"), "f107_obs"]
    f107a =  _SW.at[epoch.floor("D"), "f107_81ctr_obs"]

    rho = msise_flat(epoch_dt, altitude, latitude, longitude, f107a, f107, ap, method="gt7d")[5] # total mass density [g cm^-3]
    rho = rho * 1000 # convert to [kg m^-3]
    return rho


def accel_drag(epoch_dt, x, mass, area, Cd, T):
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
    omega = np.array([0, 0, OMEGA_EARTH])  # Angular velocity of the Earth [rad/s]

    # Position and velocity in true-of-date system
    r_tod = np.dot(T, x[:3])
    v_tod = np.dot(T, x[3:6])

    # Velocity relative to the Earth's atmosphere
    v_rel = v_tod - np.cross(omega, r_tod)
    v_abs = np.linalg.norm(v_rel)

    r_eci = x[0:3]
    r_ecef = T @ r_eci

    longitude, latitude, altitude = coordinates.sECEFtoGEOC(r_ecef, use_degrees="true")
    rho = compute_density_nrlmsise00(epoch_dt, altitude / 1000, latitude, longitude)

    # Acceleration
    a_tod = -0.5 * Cd * (area / mass) * rho * v_abs * v_rel
    a_drag = np.dot(T.T, a_tod)

    return a_drag


