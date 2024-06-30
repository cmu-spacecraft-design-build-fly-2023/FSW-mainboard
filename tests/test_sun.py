import numpy as np
import pytest

import tests.cp_mock  # noqa: F401
from flight.apps.sun import compute_body_sun_vector_from_lux

MAX_RANGE_OPT4001 = 117000


# TODO - use realistics values
@pytest.mark.parametrize(
    "I_vec, expected",
    [
        (
            [80000, 0, 30000, 0, 0, 20000],
            [0.91168461, 0.34188173, -0.22792115],
        ),
        ([117000, 0, 0, 0, 0, 0], [1.0, 0.0, 0.0]),
        ([0, 117000, 0, 0, 0, 0], [-1.0, 0.0, 0.0]),
        ([0, 0, 117000, 0, 0, 0], [0.0, 1.0, 0.0]),
        ([0, 0, 0, 117000, 0, 0], [0.0, -1.0, 0.0]),
        ([0, 0, 0, 0, 117000, 0], [0.0, 0.0, 1.0]),
        ([0, 0, 0, 0, 0, 117000], [0.0, 0.0, -1.0]),
        ([0, 0, 0, 0, 0, 0], [0.0, 0.0, 0.0]),  # Edge case: all zeros
        (
            [500, 500, 500, 500, 500, 500],
            [0.0, 0.0, 0.0],
        ),  # Edge case: equal flux on all faces (impossible though)
    ],
)
def test_compute_body_sun_vector(I_vec, expected):
    result = compute_body_sun_vector_from_lux(I_vec)
    assert result == pytest.approx(expected, rel=1e-6)


def in_eclipse(sun_vector, x_pos_eci):
    """
    Computes the illumination fraction of a satellite in Earth orbit using a
    cylindrical Earth shadow model.

    Parameters:
        sun_vector (np.array): Sun vector in inertial frame.
        x_pos_eci (np.array): Position of the satellite in the ECI frame.

    Returns:
        illumination_param (float): Illumination fraction (0 <= nu <= 1). nu = 0 means spacecraft in complete shadow,
        nu = 1 mean spacecraft fully illuminated by sun.

    References:
    1. O. Montenbruck, and E. Gill, Satellite Orbits: Models, Methods
                                    and Applications_, 2012, p.80-83.
    """
    # Projection of spacecraft position
    s = np.dot(x_pos_eci, sun_vector)

    # Compute illumination parameter
    illumination_param = True
    if (
        s / np.linalg.norm(s) >= 1.0
        or np.linalg.norm(x_pos_eci - s * sun_vector) > 6378.0e3
    ):
        illumination_param = False

    return illumination_param


if __name__ == "__main__":
    pytest.main()
