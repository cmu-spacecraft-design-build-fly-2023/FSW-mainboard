"""

Attitude Determination Module for the Attitude Determination and Control Subsystem (ADCS).

This module is responsible for processing GNC sensor data to determine the satellite's attitude.

Argus possesses a 3-axis IMU (Inertial Measurement Unit) providing angular rate, acceleration, and
magnetic field data on the mainboard. A Star Tracker is also present on the Z- face if the spacecraft,
providing attitude quaternion at X Hz for fine attitude determination.

"""
