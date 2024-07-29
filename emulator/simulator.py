from datetime import datetime

from simulation.argusloop.spacecraft import Spacecraft


class Simulator:
    def __init__(self):
        self.epoch_time = datetime.now()
        self.dt = 1.0
        config = {
            "mass": 2.0,
            "inertia": [10, 20, 30, 0.0, 0.0, 0.0],
            "dt": self.dt,
            "epoch": self.epoch_time,
            "initial_attitude": [1.0, 0, 0, 0, 0.1, -0.2, 0.3],
            "initial_orbit_oe": [6.92e6, 0, 0, 0, 0, 0],
            "gravity_order": 5,
            "gravity_degree": 5,
            "drag": True,
            "third_body": True,
        }
        self.time = self.epoch_time
        # self.u = np.zeros(3)

        self.spacecraft = Spacecraft(config)

    # def advance_to_time(self, time: datetime):
    #     time_diff = time - self.time
    #     secs = time_diff.total_seconds()
    #     iters = int(secs / self.dt)
    #     for _ in range(iters):
    #         self.spacecraft.advance(self.u)
    #     self.time += timedelta(seconds=(iters * self.dt))
