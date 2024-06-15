from brahe import frames, coordinates
import pyIGRF

import numpy as np
import numpy as np

def get_magnetic_field_ECI(epoch, x):

    r_ecef = frames.sECEFtoECI(epoch, x)
    longitude, latitude, altitude = coordinates.sECEFtoGEOC(r_ecef[0:3], use_degrees="true")

    """ Returns: 
        D is declination (+ve east)
        I is inclination (+ve down)
        H is horizontal intensity
        X is north component
        Y is east component
        Z is vertical component (+ve down)
        F is total intensity """
    # North-East-Down (NED) frame
    _, _, _, BN, BE, BD, _ = pyIGRF.igrf_value(latitude, longitude, altitude/1000, epoch.year()) # Need altitue in km

    NED_nT = np.array([[BN], [BE], [-BD]]) # nanoTesla
    
    # NED to ECEF
    B_ECEF_nT = ROT_NED2ECEF(longitude, latitude) @ NED_nT
    # ECEF to ECI
    B_ECI_nT = frames.sECEFtoECI(epoch, B_ECEF_nT.flatten())

    # Frame transformation to ECI and conversion to Tesla
    B_ECI_nT = B_ECI_nT * 1e-9

    return B_ECI_nT



def ROT_NED2ECEF(longitude, latitude):
    # Takes degrees

    ϕ = np.radians(latitude)
    λ = np.radians(longitude)

    NED2ECEF_Q = np.array([[-np.sin(ϕ)*np.cos(λ), -np.sin(λ), -np.cos(ϕ)*np.cos(λ)],
                            [-np.sin(ϕ)*np.sin(λ), np.cos(λ), -np.cos(ϕ)*np.sin(λ)],
                            [np.cos(ϕ), 0.0, -np.sin(ϕ)]])

    return NED2ECEF_Q

