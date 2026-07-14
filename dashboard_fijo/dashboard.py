import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from simulator import DroneSimulator
from config import *


class Dashboard:

    def __init__(self):

        # ---------------------------------
        # Simulador
        # ---------------------------------

        self.sim = DroneSimulator()

        # Valores iniciales del PID

        self.kp = KP
        self.ki = KI
        self.kd = KD

        # ---------------------------------
        # Estado de perturbaciones
        # ---------------------------------

        self.gust = False

        self.wind = False

        self.turbulence = False

        # ---------------------------------
        # Ventana
        # ---------------------------------

        self.fig = plt.figure(figsize=(15, 9))

        self.fig.canvas.manager.set_window_title(
            "Control de Roll de un Drone"
        )

        # ---------------------------------
        # Título
        # ---------------------------------

        self.fig.suptitle(
            "Simulador de Control PID del Roll",
            fontsize=16,
            fontweight="bold"
        )

        # ---------------------------------
        # Cuatro gráficos
        # ---------------------------------

        self.ax_roll = plt.subplot2grid(
            (4, 2),
            (0, 0)
        )

        self.ax_error = plt.subplot2grid(
            (4, 2),
            (1, 0)
        )

        self.ax_torque = plt.subplot2grid(
            (4, 2),
            (2, 0)
        )

        self.ax_dist = plt.subplot2grid(
            (4, 2),
            (3, 0)
        )

        # ---------------------------------
        # Panel derecho
        # ---------------------------------

        self.ax_panel = plt.subplot2grid(
            (4, 2),
            (0, 1),
            rowspan=4
        )

        self.ax_panel.axis("off")

        self.ax_panel.text(
            0.05,
            0.95,
            "CONTROLADOR PID",
            fontsize=16,
            weight="bold"
        )

        self.txt_kp = self.ax_panel.text(
            0.05,
            0.88,
            f"KP = {self.kp:.5f}",
            fontsize=12
        )

        self.txt_ki = self.ax_panel.text(
            0.05,
            0.84,
            f"KI = {self.ki:.5f}",
            fontsize=12
        )

        self.txt_kd = self.ax_panel.text(
            0.05,
            0.80,
            f"KD = {self.kd:.5f}",
            fontsize=12
        )

        # ---------------------------------
        # Datos de prueba
        # ---------------------------------

        self.t = np.arange(
            0,
            TIME,
            DT
        )

        self.roll = np.zeros_like(self.t)

        self.error = np.zeros_like(self.t)

        self.torque = np.zeros_like(self.t)

        self.dist = np.zeros_like(self.t)

        # ---------------------------------
        # Líneas
        # ---------------------------------

        self.line_roll, = self.ax_roll.plot(
            self.t,
            self.roll,
            lw=2
        )

        self.line_error, = self.ax_error.plot(
            self.t,
            self.error,
            lw=2
        )

        self.line_torque, = self.ax_torque.plot(
            self.t,
            self.torque,
            lw=2
        )

        self.line_dist, = self.ax_dist.plot(
            self.t,
            self.dist,
            lw=2
        )

        # ---------------------------------
        # Títulos
        # ---------------------------------

        self.ax_roll.set_title("Ángulo de Roll")

        self.ax_error.set_title("Error")

        self.ax_torque.set_title("Torque del PID")

        self.ax_dist.set_title("Perturbación")

        # ---------------------------------
        # Ejes
        # ---------------------------------

        self.ax_roll.set_ylabel("°")

        self.ax_error.set_ylabel("°")

        self.ax_torque.set_ylabel("Nm")

        self.ax_dist.set_ylabel("Nm")

        self.ax_dist.set_xlabel("Tiempo [s]")

        # ---------------------------------
        # Grillas
        # ---------------------------------

        for ax in (
                self.ax_roll,
                self.ax_error,
                self.ax_torque,
                self.ax_dist):

            ax.grid(True)

            ax.set_xlim(
                0,
                TIME
            )

    # ---------------------------------
    def create_sliders(self):

        axcolor = "lightgoldenrodyellow"

        self.ax_kp = plt.axes(
            [0.62, 0.55, 0.30, 0.03],
            facecolor=axcolor
        )

        self.ax_ki = plt.axes(
            [0.62, 0.48, 0.30, 0.03],
            facecolor=axcolor
        )

        self.ax_kd = plt.axes(
            [0.62, 0.41, 0.30, 0.03],
            facecolor=axcolor
        )

        self.slider_kp = Slider(
            self.ax_kp,
            "KP",
            0.0,
            0.15,
            valinit=self.kp,
            valstep=0.0005
        )

        self.slider_ki = Slider(
            self.ax_ki,
            "KI",
            0.0,
            0.50,
            valinit=self.ki,
            valstep=0.001
        )

        self.slider_kd = Slider(
            self.ax_kd,
            "KD",
            0.0,
            0.05,
            valinit=self.kd,
            valstep=0.0001
        )

        self.slider_kp.on_changed(self.update_pid)

        self.slider_ki.on_changed(self.update_pid)

        self.slider_kd.on_changed(self.update_pid)
    def create_buttons(self):

        self.ax_gust = plt.axes(
            [0.66,0.28,0.20,0.05]
        )

        self.ax_wind = plt.axes(
            [0.66,0.21,0.20,0.05]
        )

        self.ax_turb = plt.axes(
            [0.66,0.14,0.20,0.05]
        )

        self.ax_reset = plt.axes(
            [0.66,0.05,0.20,0.05]
        )

        self.btn_gust = Button(
            self.ax_gust,
            "Ráfaga"
        )

        self.btn_wind = Button(
            self.ax_wind,
            "Cambio Viento"
        )

        self.btn_turb = Button(
            self.ax_turb,
            "Turbulencia"
        )

        self.btn_reset = Button(
            self.ax_reset,
            "Reset"
        )

        self.btn_gust.on_clicked(
            self.click_gust
        )

        self.btn_wind.on_clicked(
            self.click_wind
        )

        self.btn_turb.on_clicked(
            self.click_turbulence
        )

        self.btn_reset.on_clicked(
            self.click_reset
        )

    def click_gust(self,event):

        self.gust = not self.gust

        color = (
            "lightgreen"
            if self.gust
            else "0.85"
        )

        self.ax_gust.set_facecolor(color)

        self.simulate_system()

    def click_wind(self,event):

        self.wind = not self.wind

        color = (
            "lightgreen"
            if self.wind
            else "0.85"
        )

        self.ax_wind.set_facecolor(color)

        self.simulate_system()

    def click_turbulence(self,event):

        self.turbulence = not self.turbulence

        color = (
            "lightgreen"
            if self.turbulence
            else "0.85"
        )

        self.ax_turb.set_facecolor(color)

        self.simulate_system()

    def click_reset(self,event):

        self.gust = False

        self.wind = False

        self.turbulence = False

        self.slider_kp.reset()

        self.slider_ki.reset()

        self.slider_kd.reset()

        self.ax_gust.set_facecolor("0.85")

        self.ax_wind.set_facecolor("0.85")

        self.ax_turb.set_facecolor("0.85")

        self.simulate_system()

    def simulate_system(self):

        data = self.sim.simulate(

            self.kp,

            self.ki,

            self.kd,

            gust=self.gust,

            wind=self.wind,

            turbulence=self.turbulence

        )

        self.t = data["t"]

        self.roll = np.degrees(data["roll"])

        self.error = np.degrees(data["error"])

        self.torque = data["torque"]

        self.dist = data["disturbance"]

        self.update_plots()
    def update_plots(self):

        # -----------------------------
        # Roll
        # -----------------------------

        self.line_roll.set_data(
            self.t,
            self.roll
        )

        self.ax_roll.relim()

        self.ax_roll.autoscale_view()

        # -----------------------------
        # Error
        # -----------------------------

        self.line_error.set_data(
            self.t,
            self.error
        )

        self.ax_error.relim()

        self.ax_error.autoscale_view()

        # -----------------------------
        # Torque
        # -----------------------------

        self.line_torque.set_data(
            self.t,
            self.torque
        )

        self.ax_torque.relim()

        self.ax_torque.autoscale_view()

        # -----------------------------
        # Perturbación
        # -----------------------------

        self.line_dist.set_data(
            self.t,
            self.dist
        )

        self.ax_dist.relim()

        self.ax_dist.autoscale_view()

        self.fig.canvas.draw_idle()

    def update_pid(self, value):

        self.kp = self.slider_kp.val

        self.ki = self.slider_ki.val

        self.kd = self.slider_kd.val

        self.txt_kp.set_text(
            f"KP = {self.kp:.5f}"
        )

        self.txt_ki.set_text(
            f"KI = {self.ki:.5f}"
        )

        self.txt_kd.set_text(
            f"KD = {self.kd:.5f}"
        )

        self.simulate_system()

    def run(self):

        self.create_sliders()

        self.create_buttons()

        self.simulate_system()

        plt.tight_layout()

        plt.show()