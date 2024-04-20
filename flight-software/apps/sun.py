import math


def process_sun_vector(raw_readings, prev_sun_vec):

    # TODO Should process the raw readings to determine the sun vector
    angle = math.radians(0.01)  # Rotation angle

    eclipse_state = in_eclipse(raw_readings)

    # The following is for testing purposes (demo)
    new_x = prev_sun_vec[0] * math.cos(angle) - prev_sun_vec[1] * math.sin(angle)
    new_y = prev_sun_vec[0] * math.sin(angle) + prev_sun_vec[1] * math.cos(angle)
    sun_vec = [new_x, new_y, prev_sun_vec[2]]

    magnitude = math.sqrt(sum(component**2 for component in sun_vec))
    sun_vec = [sun_vec[0] / magnitude, sun_vec[1] / magnitude, sun_vec[2] / magnitude]

    return sun_vec, eclipse_state


def in_eclipse(readings):
    # Should process the raw readings to determine the eclipse state
    eclipse_state = True
    return eclipse_state
