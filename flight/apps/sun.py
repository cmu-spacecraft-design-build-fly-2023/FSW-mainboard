from hal.configuration import SATELLITE

def read_light_sensors():
    """
    Read the light sensors on the x+,x-,y+,y-, and z+ faces of the satellite

    Returns:
        lux_readings: list of lux readings on each face
    """

    sensor_faces = [
        'LIGHT_SENSOR_XP',
        'LIGHT_SENSOR_XM',
        'LIGHT_SENSOR_YP',
        'LIGHT_SENSOR_YM',
        'LIGHT_SENSOR_ZP'
    ]
    
    lux_readings = []

    for face in sensor_faces:
        try:
            s = getattr(SATELLITE, face).lux()
            lux_readings.append(s)
        except AttributeError as e:
            #logging.error(f"AttributeError for {face}: {e}")
            print(f"AttributeError for {face}: {e}")
            lux_readings.append(None)
        except Exception as e:
            #logging.error(f"Error reading {face}: {e}")
            print(f"Error reading {face}: {e}")
            lux_readings.append(None)


    # Read the z- face - not implemented in the HAL yet

    return lux_readings


def compute_body_sun_vector(I_vec):
    """
    Get unit sun vector expressed in the body frame from solar flux values.

    Args:
        I_vec: flux values on each face in the following order
        - X+ face, X- face, Y+ face, Y- face, Z+ face

    Returns:
        sun_body: unit vector from spacecraft to sun expressed in body frame
    """

    status = False

    sun_body = [I_vec[0] - I_vec[1], I_vec[2] - I_vec[3], I_vec[4]]

    norm = (sun_body[0] ** 2 + sun_body[1] ** 2 + sun_body[2] ** 2) ** 0.5

    # Normalize the vector if the norm is not zero
    if norm != 0:
        sun_body = [x / norm for x in sun_body]
        status = True

    return status, sun_body


def in_eclipse(raw_readings):
    """
    Check the eclipse conditions based on the lux readings

    Parameters:


    Returns:

    """
    # TODO
    return False
