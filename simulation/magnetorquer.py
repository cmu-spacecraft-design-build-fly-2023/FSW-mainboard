import numpy as np


COPPER_RESISTIVITY = 1.724 * 10**-8

# Update attributes with final design 
# This is a single torquer
class Magnetorquer:
    def __init__(self, 
                max_voltage = 5, 
                coils_per_layer = 32.0,
                layers = 2.0,
                trace_width = 0.0007317, # m
                gap_width = 8.999 * 10**-5, # m
                trace_thickness = 3.556 * 10**-5, # 1oz copper - 35um = 1.4 mils
                max_current_rating = 1, # A
                max_power = 5 # W
                ):
        self.max_voltage = max_voltage
        self.N = coils_per_layer
        self.pcb_layers = layers
        self.N_per_face = coils_per_layer * layers
        self.trace_thickness = trace_thickness
        self.trace_width = trace_width
        self.gap_width = gap_width
        self.coil_width = trace_width + gap_width
        self.max_power = max_power
        self.max_current_rating = max_current_rating
        self.max_current = max_power / max_voltage

        self.pcb_side_max = 0.1
        self.A_cross = (self.pcb_side_max - self.N * self.coil_width)**2
        self.R = self.compute_coil_resistance()


    def compute_coil_resistance(self):
        coil_length = 4 * (self.pcb_side_max - self.N * self.coil_width) * self.N * self.pcb_layers 
        R = COPPER_RESISTIVITY * coil_length / (self.trace_width * self.trace_thickness)
        return R


    def set_dipole_moment_voltage(self, voltage):
        if voltage > self.max_voltage:
            raise ValueError("Voltage exceeds maximum voltage rating.")
        # Current driver is PWM 
        I = voltage / self.R
        if I > self.max_current:
            raise ValueError(f'Current exceeds maximum power limit of {self.max_power} W.') # For now, raise an error
        dipole_moment = self.N_per_face * I * self.A_cross
        return dipole_moment

    def set_dipole_moment_current(self, current):
        if current > self.max_current:
            raise ValueError(f'Current exceeds maximum power limit of {self.max_power} W.')
        dipole_moment = self.N_per_face * current * self.A_cross
        return dipole_moment



