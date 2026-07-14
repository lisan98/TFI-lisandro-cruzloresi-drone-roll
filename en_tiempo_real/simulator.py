import numpy as np

from config import *


class DroneSimulator:


    def __init__(self):

        # =====================================================
        # Parámetros físicos
        # =====================================================

        self.J = J

        self.dt = DT

        self.tau_esc = TAU_ESC

        self.tau_imu = TAU_IMU

        # =====================================================
        # Tiempo
        # =====================================================

        self.time = 0.0

        self.running = True

        self.simulation_speed = 1.0

        # =====================================================
        # Referencia
        # =====================================================

        self.reference = np.deg2rad(REFERENCE)

        # =====================================================
        # Ganancias PID
        # =====================================================

        self.kp = KP
        self.ki = KI
        self.kd = KD

        # =====================================================
        # Estados de la planta
        # =====================================================

        # Ángulo real del drone [rad]

        self.roll = 0.0

        # Velocidad angular [rad/s]

        self.roll_rate = 0.0

        # Aceleración angular [rad/s²]

        self.roll_acc = 0.0

        # =====================================================
        # Estados del controlador PID
        # =====================================================

        self.error = 0.0

        self.previous_error = 0.0

        self.integral = 0.0

        self.derivative = 0.0

        # Salida del PID

        self.pid_output = 0.0

        # =====================================================
        # Modelo del ESC
        # =====================================================

        # Salida filtrada del ESC

        self.esc_output = 0.0

        # =====================================================
        # Modelo del IMU
        # =====================================================

        # Ángulo medido por el sensor

        self.imu_roll = 0.0

        # =====================================================
        # Torque aplicado
        # =====================================================

        self.control_torque = 0.0

        # =====================================================
        # Perturbaciones
        # =====================================================

        self.disturbance = 0.0

        self.disturbance_amplitude = DIST_AMPLITUDE

        self.gust_active = False

        self.wind_active = False

        self.turbulence_active = False

        self.gust_duration = 0.20

        self.gust_time_left = 0.0

        # =====================================================
        # Historial (dashboard)
        # =====================================================

        self.t_history = []

        self.roll_history = []

        self.error_history = []

        self.torque_history = []

        self.disturbance_history = []

        # cantidad máxima de puntos
        self.max_points = MAX_POINTS

    def set_pid(self, kp, ki, kd):

        self.kp = kp
        self.ki = ki
        self.kd = kd

    def set_reference(self, angle_deg):

        self.reference = np.deg2rad(angle_deg)

    def set_disturbance_amplitude(self, amplitude):

        self.disturbance_amplitude = amplitude

    def enable_gust(self):

        self.gust_active = True

        self.gust_time_left = self.gust_duration

    def enable_turbulence(self):

        self.turbulence_active = not self.turbulence_active

    def enable_wind(self):

        self.wind_active = not self.wind_active


    def step(self):
        if not self.running:
            return
        # =====================================================
        # 1. Lectura del IMU
        # =====================================================

        measured_roll = self.imu_roll

        # =====================================================
        # 2. Error
        # =====================================================

        self.error = self.reference - measured_roll

        # =====================================================
        # 3. PID
        # =====================================================

        self.integral += self.error * self.dt

        self.derivative = (
            self.error - self.previous_error
        ) / self.dt

        self.pid_output = (

            self.kp * self.error +

            self.ki * self.integral +

            self.kd * self.derivative

        )

        self.previous_error = self.error

        # =====================================================
        # 4. Modelo del ESC
        # Primer orden
        # =====================================================

        self.esc_output += (

            self.pid_output -

            self.esc_output

        ) * self.dt / self.tau_esc

        self.esc_output = np.clip(
            self.esc_output,
            -MAX_TORQUE,
            MAX_TORQUE
        )

        # =====================================================
        # 5. Perturbaciones
        # =====================================================

        disturbance = 0.0

        # ---------- Ráfaga ----------

        if self.gust_active:

            disturbance += self.disturbance_amplitude

            self.gust_time_left -= self.dt

            if self.gust_time_left <= 0:

                self.gust_active = False

        # ---------- Viento ----------

        if self.wind_active:

            disturbance += (

                0.5 *

                self.disturbance_amplitude

            )

        # ---------- Turbulencia ----------

        if self.turbulence_active:

            disturbance += (

                self.disturbance_amplitude *

                np.sin(

                    2 * np.pi *

                    TURB_FREQUENCY *

                    self.time

                )

            )

        self.disturbance = disturbance

        # =====================================================
        # 6. Torque total
        # =====================================================

        self.control_torque = (

            self.esc_output +

            self.disturbance

        )

        # =====================================================
        # 7. Aceleración angular
        # =====================================================

        self.roll_acc = (

            self.control_torque /

            self.J

        )

        # =====================================================
        # 8. Velocidad angular
        # =====================================================

        self.roll_rate += (

            self.roll_acc *

            self.dt

        )

        # =====================================================
        # 9. Ángulo de Roll
        # =====================================================

        self.roll += (

            self.roll_rate *

            self.dt

        )

        # =====================================================
        # 10. Modelo del IMU
        # Sensor de primer orden
        # =====================================================

        self.imu_roll += (

            self.roll -

            self.imu_roll

        ) * self.dt / self.tau_imu

        # =====================================================
        # 11. Tiempo
        # =====================================================

        self.time += self.dt

        # =====================================================
        # Historial
        # =====================================================

        self.t_history.append(self.time)

        self.roll_history.append(np.degrees(self.roll))

        self.error_history.append(np.degrees(self.error))

        self.torque_history.append(self.control_torque)

        self.disturbance_history.append(self.disturbance)

        # Mantener una ventana móvil
        if len(self.t_history) > self.max_points:

            self.t_history.pop(0)

            self.roll_history.pop(0)

            self.error_history.pop(0)

            self.torque_history.pop(0)

            self.disturbance_history.pop(0)

    def get_data(self):
        return {
            "time": self.t_history,
            "roll": self.roll_history,
            "error": self.error_history,
            "torque": self.torque_history,
            "disturbance": self.disturbance_history,

            "current_time": self.time,
            "current_roll": self.roll,
            "current_error": self.error,
            "current_torque": self.control_torque,
            "current_imu": self.imu_roll,
            "current_speed": self.roll_rate,
            "current_acc": self.roll_acc,
            "current_state": "RUNNING" if self.running else "PAUSED",
        }
    
    def reset(self):

        self.running = True

        self.time = 0.0

        self.roll = 0.0

        self.roll_rate = 0.0

        self.roll_acc = 0.0

        self.error = 0.0

        self.previous_error = 0.0

        self.integral = 0.0

        self.derivative = 0.0

        self.pid_output = 0.0

        self.esc_output = 0.0

        self.imu_roll = 0.0

        self.control_torque = 0.0

        self.disturbance = 0.0

        self.gust_active = False

        self.wind_active = False

        self.turbulence_active = False

        self.gust_time_left = 0.0

        self.t_history.clear()

        self.roll_history.clear()

        self.error_history.clear()

        self.torque_history.clear()

        self.disturbance_history.clear()

    def clear_disturbances(self):

        self.gust_active = False

        self.wind_active = False

        self.turbulence_active = False

        self.gust_time_left = 0.0

        self.disturbance = 0.0

    def set_disturbance_amplitude(self, value):

        self.disturbance_amplitude = value

    def set_gust_duration(self, duration):

        self.gust_duration = duration

    def play(self):

        self.running = True


    def pause(self):

        self.running = False