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


def compute_body_sun_vector_from_lux(I_vec):
    """
    Get unit sun vector expressed in the body frame from solar flux values.

    Args:
        I_vec: flux values on each face in the following order
        - X+ face, X- face, Y+ face, Y- face, Z+ face

    Returns:
        sun_body: unit vector from spacecraft to sun expressed in body frame
    """

    status = False
    sun_body = [0, 0, 0]

    num_valid_readings = len(I_vec) - I_vec.count(None)

    if num_valid_readings >= 3: # only if unique determination is possible

        for i in range(len(I_vec)): # if None replace with 0 to cancel
            if I_vec[i] is None:
                I_vec[i] = 0
        
        sun_body[0] = I_vec[0] - I_vec[1]
        sun_body[1] = I_vec[2] - I_vec[3]
        sun_body[2] = I_vec[4]

        norm = (sun_body[0] ** 2 + sun_body[1] ** 2 + sun_body[2] ** 2) ** 0.5

        # Normalize the vector if the norm is not zero
        if norm != 0:
            sun_body[0] = sun_body[0] / norm
            sun_body[1] = sun_body[1] / norm
            sun_body[2] = sun_body[2] / norm
            
            status = True

    return status, sun_body



def in_eclipse(raw_readings, threshold_lux_illumination=1000):
    """
    Check the eclipse conditions based on the lux readings

    Parameters:
        raw_readings (list): list of lux readings on each face (X+ face, X- face, Y+ face, Y- face, Z+ face)
        
    Returns:
        eclipse (bool): True if the satellite is in eclipse, False otherwise

    """
    eclipse = False
    for reading in raw_readings:
        if reading is not None and reading < threshold_lux_illumination:
            eclipse = True
    return eclipse
