import numpy as np
import pytest

import tests.cp_mock  # noqa: F401
from flight.apps.sun import compute_body_sun_vector_from_lux, in_eclipse, SUN_VECTOR_STATUS




@pytest.mark.parametrize(
    "I_vec, expected",
    [
        ([80000, 0, 30000, 0, 0], (SUN_VECTOR_STATUS.UNIQUE_DETERMINATION, [0.91168461, 0.34188173, 0.0])),
        ([117000, 0, 0, 0, 0], (SUN_VECTOR_STATUS.UNIQUE_DETERMINATION, [1.0, 0.0, 0.0])),
        ([0, 117000, 0, 0, 0], (SUN_VECTOR_STATUS.UNIQUE_DETERMINATION, [-1.0, 0.0, 0.0])),
        ([0, 0, 117000, 0, 0], (SUN_VECTOR_STATUS.UNIQUE_DETERMINATION, [0.0, 1.0, 0.0])),
        ([0, 0, 0, 117000, 0], (SUN_VECTOR_STATUS.UNIQUE_DETERMINATION, [0.0, -1.0, 0.0])),
        ([0, 0, 0, 0, 117000], (SUN_VECTOR_STATUS.UNIQUE_DETERMINATION, [0.0, 0.0, 1.0])),
        ([None, 117000, 0, 0, 0], (SUN_VECTOR_STATUS.MISSING_XP_READING, [1.0, 0, 0])),
        ([0, None, 0, 117000, 0], (SUN_VECTOR_STATUS.MISSING_XM_READING, [0.0, -1.0, 0.0])),
        ([None, 20000, 0, None, None], (SUN_VECTOR_STATUS.NOT_ENOUGH_READINGS, [-1.0, 0.0, 0.0])),
        ([None, None, None, None, None], (SUN_VECTOR_STATUS.NO_READINGS, [0.0, 0.0, 0.0])),
    ],
)
def test_compute_body_sun_vector_from_lux(I_vec, expected):
    result = compute_body_sun_vector_from_lux(I_vec)
    assert result[0] == expected[0]
    assert result[1] == pytest.approx(expected[1], rel=1e-6)


@pytest.mark.parametrize("raw_readings, threshold_lux_illumination, expected",
[
    ([2000, 3000, 2500, 4000, 3500], 1000, False), # All readings are above threshold
    ([500, 600, 700, 400, 550], 1000, True), # All readings are below threshold
    ([2000, 300, 2500, 400, 3500], 1000, True), # Aboove and below threshold
    ([None, None, None, None, None], 1000, False) # All readings are None
],)
def test_in_eclipse(raw_readings, threshold_lux_illumination, expected):
    assert in_eclipse(raw_readings, threshold_lux_illumination) == expected




if __name__ == "__main__":
    pytest.main()
