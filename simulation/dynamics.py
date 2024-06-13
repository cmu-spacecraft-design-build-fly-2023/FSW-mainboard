import numpy as np

from simulation.transformations import L


def quat_kinematics(q, ω):
    H = np.vstack([np.zeros(3), np.eye(3)])  # TODO reformulate to avoid the allocation
    q̇ = 0.5 * L(q) @ H @ ω
    return q̇


def euler_rotational_dynamics(params, ω, τ):
    return np.linalg.inv(params.J).dot(τ - np.cross(ω, np.dot(params.J, ω)))


def attitude_dynamics(params, rot_state):
    xdot = np.zeros(7)
    xdot[0:4] = quat_kinematics(rot_state[0:4])
    xdot[4:7] = euler_rotational_dynamics(params, rot_state[4:7])
    return xdot


def rk4(dynamics, x, u, dt):
    k1 = dt * dynamics(x, u)
    k2 = dt * dynamics(x + k1 * 0.5, u)
    k3 = dt * dynamics(x + k2 * 0.5, u)
    k4 = dt * dynamics(x + k3, u)
    x = x + (1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return x
