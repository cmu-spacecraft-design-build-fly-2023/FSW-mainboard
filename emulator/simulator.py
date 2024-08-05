from datetime import datetime, timedelta

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
            "gravity_order": 10,
            "gravity_degree": 10,
            "drag": True,
            "third_body": True,
        }
        print(f"Here is the current satellite configuration:\n{config}")
        change_config = input("Would you like to modify the config? (y/n)") == "y"
        if change_config:
            config["mass"] = self.get_float_input("mass:")
            config["inertia"] = self.get_matrix_input("inertia matrix: ", 6)
            config["dt"] = self.get_float_input("dt:")
            config["initial_attitude"] = self.get_matrix_input("initial_attitude: ", 7)
            config["initial_orbit_oe"] = self.get_matrix_input("initial_orbit_oe: ", 6)
            config["gravity_order"] = self.get_int_input("gravity_order:")
            config["gravity_degree"] = self.get_int_input("gravity_degree:")
            config["drag"] = input("drag? (y/n)") == "y"
            config["third_body"] = input("third_body? (y/n)") == "y"
        self.time = self.epoch_time

        self.spacecraft = Spacecraft(config)

    def advance_to_time(self, time: datetime):
        time_diff = time - self.time
        secs = time_diff.total_seconds()
        iters = int(secs / self.dt)
        for _ in range(iters):
            self.spacecraft.advance([0.0, 0.0, 0.0])
        self.time += timedelta(seconds=(iters * self.dt))

    def get_float_input(self, prompt) -> float:
        raw = input(prompt)
        try:
            f_input = float(raw)
        except ValueError:
            print("could not interpret input as float, please try a different input")
            self.get_float_input(prompt)
        return f_input

    def get_int_input(self, prompt) -> int:
        raw = input(prompt)
        try:
            i_input = int(raw)
        except ValueError:
            print("could not interpret input as int, please try a different input")
            self.get_int_input(prompt)
        return i_input

    def get_matrix_input(self, prompt, length):
        print("please input your list in the following form. ',' indicates the end of an entry.")
        print("For Example: 1,2,3,4,5,6,7,8,9 corresponds to: [1, 2, 3, 4, 5, 6, 7, 8, 9]")
        raw = input(prompt)
        matrix = raw.split(",")
        for idx, entry in enumerate(matrix):
            try:
                matrix[idx] = float(entry)
            except ValueError:
                print("could not interpret input as float, please try a different input")
                self.get_matrix_input(prompt, length)
        assert len(matrix) == length
        return matrix
