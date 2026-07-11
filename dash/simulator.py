import numpy as np
import control as ctrl

from config import *


class DroneSimulator:

    def __init__(self):

        self.time = TIME
        self.dt = DT

        self.J = J

        self.tau_esc = TAU_ESC
        self.tau_imu = TAU_IMU

        self.reference = 0

    # ----------------------------------------------------
    # Construcción del modelo
    # ----------------------------------------------------

    def build_model(self, kp, ki, kd):

        G = ctrl.tf(
            [1],
            [self.J, 0, 0]
        )

        ESC = ctrl.tf(
            [1],
            [self.tau_esc, 1]
        )

        H = ctrl.tf(
            [1],
            [self.tau_imu, 1]
        )

        C = ctrl.tf(
            [kd, kp, ki],
            [1, 0]
        )

        T = ctrl.feedback(
            C * ESC * G,
            H
        )

        Td = ctrl.minreal(
            G / (1 + C * ESC * G * H)
        )

        return G, ESC, H, C, T, Td

    # ----------------------------------------------------
    # Vector tiempo
    # ----------------------------------------------------

    def create_time(self):

        return np.arange(
            0,
            self.time,
            self.dt
        )

    # ----------------------------------------------------
    # Referencia
    # ----------------------------------------------------

    def create_reference(self, t):

        r = np.zeros_like(t)

        r[:] = np.deg2rad(
            self.reference
        )

        return r

    # ----------------------------------------------------
    # Perturbaciones
    # ----------------------------------------------------

    def create_disturbance(
        self,
        t,
        gust=False,
        wind=False,
        turbulence=False
    ):

        dist = np.zeros_like(t)

        # --------------------------

        if gust:

            dist[
                (t >= 2) &
                (t <= 2.2)
            ] += 0.002

        # --------------------------

        if wind:

            dist += (
                0.001 *
                (0.5 * t - 0.5) *
                (t > 4) *
                (t < 6)
            )

        # --------------------------

        if turbulence:

            dist += (
                0.003 *
                np.sin(6 * t) *
                (t > 8) *
                (t < 10)
            )

        return dist

    # ----------------------------------------------------
    # Simulación
    # ----------------------------------------------------

    def simulate(

            self,

            kp,
            ki,
            kd,

            gust=False,
            wind=False,
            turbulence=False

    ):

        (
            G,
            ESC,
            H,
            C,
            T,
            Td

        ) = self.build_model(
            kp,
            ki,
            kd
        )

        t = self.create_time()

        r = self.create_reference(t)

        # --------------------------
        # Referencia
        # --------------------------

        resp = ctrl.forced_response(
            T,
            t,
            r
        )

        y = resp.outputs

        # --------------------------
        # Perturbaciones
        # --------------------------

        dist = self.create_disturbance(
            t,
            gust,
            wind,
            turbulence
        )

        resp_d = ctrl.forced_response(
            Td,
            t,
            dist
        )

        yd = resp_d.outputs

        # --------------------------
        # Salida total
        # --------------------------

        y_total = y + yd

        # --------------------------
        # Error
        # --------------------------

        error = r - y_total

        # --------------------------
        # Torque PID
        # --------------------------

        # Error

        error = r - y_total

        # Integral

        integral = np.cumsum(error) * self.dt

        # Derivada

        derivative = np.gradient(error, self.dt)

        # Salida del PID (torque de control)

        torque = (
            kp * error
            + ki * integral
            + kd * derivative
        )

        return {

            "t": t,

            "reference": r,

            "roll": y_total,

            "error": error,

            "torque": torque,

            "disturbance": dist,

            "controller": C,

            "plant": G,

            "closed_loop": T,

            "disturbance_tf": Td,

            "poles": ctrl.poles(T)

        }