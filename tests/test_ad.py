import pytest

import tests.cp_mock  # noqa: F401
from flight.apps.ad import TRIAD


@pytest.mark.parametrize(
    "n1, n2, b1, b2, expected",
    [
        (
            [1, 0, 0.0],
            [0.6, 0.8, 0.0],
            [0.9622641509433965, -0.22641509433962265, -0.15094339622641512],
            [0.69811320754717, 0.5886792452830192, -0.40754716981132083],
            [0.9712858623572642, 0.19425717247145274, -0.09712858623572641, 0.0971285862357264],
        )
    ],
)
def test_TRIAD(n1, n2, b1, b2, expected):
    result = TRIAD(n1, n2, b1, b2)
    assert result == pytest.approx(expected, rel=1e-6)
