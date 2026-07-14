import numpy as np
import time
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSlider,
    QStatusBar
)

from PyQt5.QtCore import Qt, QTimer

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas
)

from matplotlib.figure import Figure

from simulator import DroneSimulator

from config import *


class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        #--------------------------------------
        # Simulador
        #--------------------------------------

        self.sim = DroneSimulator()

        #--------------------------------------
        # Configuración ventana
        #--------------------------------------

        self.setWindowTitle(
            "Drone Roll Control Simulator"
        )

        self.resize(
            1700,
            950
        )

        #--------------------------------------
        # Timer
        #--------------------------------------

        self.timer = QTimer()

        self.timer.setInterval(
            UPDATE_INTERVAL
        )

        self.timer.timeout.connect(
            self.update_simulation
        )

        #--------------------------------------
        # Layout principal
        #--------------------------------------

        self.main_layout = QHBoxLayout()

        self.setLayout(
            self.main_layout
        )

        #===================================================
        # PANEL IZQUIERDO
        #===================================================

        self.left_panel = QVBoxLayout()

        self.main_layout.addLayout(
            self.left_panel,
            stretch=5
        )

        #===================================================
        # PANEL DERECHO
        #===================================================

        self.right_panel = QVBoxLayout()

        self.main_layout.addLayout(
            self.right_panel,
            stretch=1
        )

        #===================================================
        # TOOLBAR
        #===================================================

        self.create_toolbar()

        #===================================================
        # SLIDERS
        #===================================================

        self.create_sliders()

        #===================================================
        # BOTONES
        #===================================================

        self.create_buttons()

        #===================================================
        # GRÁFICOS
        #===================================================

        self.create_plots()

        #===================================================
        # PANEL DERECHO
        #===================================================

        self.create_info_panel()

        #===================================================
        # Arrancar timer
        #===================================================

        self.timer.start()

        #=========================================
        # FPS
        #=========================================

        self.last_frame = time.time()

        self.frame_counter = 0

        self.fps = 0

        #=========================================
        # Barra de estado
        #=========================================

        self.create_statusbar()

    #===========================================================
    # TOOLBAR
    #===========================================================

    def create_toolbar(self):

        toolbar = QFrame()

        toolbar.setFrameShape(
            QFrame.StyledPanel
        )

        layout = QHBoxLayout()

        toolbar.setLayout(layout)

        title = QLabel(
            "Drone Roll Control Simulator"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        font = title.font()

        font.setPointSize(16)

        font.setBold(True)

        title.setFont(font)

        layout.addWidget(title)

        self.left_panel.addWidget(toolbar)

    #===========================================================
    # PANEL DE INFORMACIÓN
    #===========================================================

    def create_info_panel(self):

        title = QLabel(
            "Variables"
        )

        font = title.font()

        font.setPointSize(14)

        font.setBold(True)

        title.setFont(font)

        self.right_panel.addWidget(title)

        self.lbl_time = QLabel("Tiempo")

        self.lbl_roll = QLabel("Roll")

        self.lbl_error = QLabel("Error")

        self.lbl_torque = QLabel("Torque")

        self.lbl_imu = QLabel("IMU")

        self.lbl_pid = QLabel("PID")

        self.lbl_speed = QLabel("Velocidad")

        self.lbl_acc = QLabel("Aceleración")

        self.lbl_state = QLabel("Estado")

        self.right_panel.addWidget(
            self.lbl_time
        )

        self.right_panel.addWidget(
            self.lbl_roll
        )

        self.right_panel.addWidget(
            self.lbl_error
        )

        self.right_panel.addWidget(
            self.lbl_torque
        )

        self.right_panel.addWidget(
            self.lbl_imu
        )

        self.right_panel.addWidget(
            self.lbl_pid
        )

        self.right_panel.addWidget(
            self.lbl_speed
        )

        self.right_panel.addWidget(
            self.lbl_acc
        )

        self.right_panel.addWidget(
            self.lbl_state
        )

        self.right_panel.addStretch()

    #===========================================================
    # CREAR FIGURA
    #===========================================================

    def create_plots(self):

        

        
        self.figure = Figure(
            figsize=(12,10)
        )

        self.figure.set_facecolor("#f2f2f2")

        
        self.canvas = FigureCanvas(
            self.figure
        )

        self.left_panel.addWidget(
            self.canvas
        )

        self.ax_roll = self.figure.add_subplot(
            411
        )

        self.ax_error = self.figure.add_subplot(
            412
        )

        self.ax_torque = self.figure.add_subplot(
            413
        )

        self.ax_dist = self.figure.add_subplot(
            414
        )

        self.figure.subplots_adjust(
            hspace=0.45
        )

        self.line_roll, = self.ax_roll.plot([], [])
        self.line_error = self.ax_error.plot([], [])[0]
        self.line_torque = self.ax_torque.plot([], [])[0]
        self.line_dist = self.ax_dist.plot([], [])[0]

        #----------------------------------
        # Roll
        #----------------------------------

        self.line_roll, = self.ax_roll.plot(
            [],
            [],
            color="tab:blue",
            linewidth=2
        )

        self.ax_roll.set_title(
            "Ángulo de Roll"
        )

        self.ax_roll.set_ylabel(
            "Grados"
        )

        self.ax_roll.grid(True)

        self.ax_roll.set_ylim(
            ROLL_YMIN,
            ROLL_YMAX
        )

        #----------------------------------
        # Error
        #----------------------------------

        self.line_error, = self.ax_error.plot(
            [],
            [],
            color="tab:red",
            linewidth=2
        )

        self.ax_error.set_title(
            "Función de Error"
        )

        self.ax_error.grid(True)

        self.ax_error.set_ylabel(
            "Grados"
        )

        self.ax_error.set_ylim(
            ERROR_YMIN,
            ERROR_YMAX
        )

        #----------------------------------
        # Torque
        #----------------------------------

        self.line_torque, = self.ax_torque.plot(
            [],
            [],
            color="tab:green",
            linewidth=2
        )

        self.ax_torque.set_title(
            "Torque del Controlador"
        )

        self.ax_torque.grid(True)

        self.ax_torque.set_ylabel(
            "Nm"
        )

        self.ax_torque.set_ylim(
            TORQUE_YMIN,
            TORQUE_YMAX
        )

        #----------------------------------
        # Perturbación
        #----------------------------------

        self.line_dist, = self.ax_dist.plot(
            [],
            [],
            color="tab:orange",
            linewidth=2
        )

        self.ax_dist.set_title(
            "Torque de Perturbación"
        )

        self.ax_dist.grid(True)

        self.ax_dist.set_ylabel(
            "Nm"
        )

        self.ax_dist.set_xlabel(
            "Tiempo [s]"
        )

        self.ax_dist.set_ylim(
            DIST_YMIN,
            DIST_YMAX
        )

    #===========================================================
    # UPDATE
    #===========================================================

    def update_simulation(self):

        """
        Este método se implementará en la Parte 4.

        Por ahora solamente evita que el timer genere
        un error al iniciar la aplicación.
        """

        pass

    def create_sliders(self):

        frame = QFrame()

        layout = QGridLayout()

        frame.setLayout(layout)

        self.left_panel.addWidget(frame)

        #=========================================
        # KP
        #=========================================

        layout.addWidget(QLabel("KP"),0,0)

        self.slider_kp = QSlider(Qt.Horizontal)

        self.slider_kp.setMinimum(int(KP_MIN*10000))
        self.slider_kp.setMaximum(int(KP_MAX*10000))
        self.slider_kp.setValue(int(KP*10000))

        layout.addWidget(self.slider_kp,0,1)

        self.lbl_kp = QLabel(f"{KP:.4f}")

        layout.addWidget(self.lbl_kp,0,2)

        #=========================================
        # KI
        #=========================================

        layout.addWidget(QLabel("KI"),1,0)

        self.slider_ki = QSlider(Qt.Horizontal)

        self.slider_ki.setMinimum(int(KI_MIN*10000))
        self.slider_ki.setMaximum(int(KI_MAX*10000))
        self.slider_ki.setValue(int(KI*10000))

        layout.addWidget(self.slider_ki,1,1)

        self.lbl_ki = QLabel(f"{KI:.4f}")

        layout.addWidget(self.lbl_ki,1,2)

        #=========================================
        # KD
        #=========================================

        layout.addWidget(QLabel("KD"),2,0)

        self.slider_kd = QSlider(Qt.Horizontal)

        self.slider_kd.setMinimum(int(KD_MIN*10000))
        self.slider_kd.setMaximum(int(KD_MAX*10000))
        self.slider_kd.setValue(int(KD*10000))

        layout.addWidget(self.slider_kd,2,1)

        self.lbl_kd = QLabel(f"{KD:.4f}")

        layout.addWidget(self.lbl_kd,2,2)

        #=========================================
        # Referencia
        #=========================================

        layout.addWidget(QLabel("Referencia [°]"),3,0)

        self.slider_ref = QSlider(Qt.Horizontal)

        self.slider_ref.setMinimum(-20)

        self.slider_ref.setMaximum(20)

        self.slider_ref.setValue(REFERENCE)

        layout.addWidget(self.slider_ref,3,1)

        self.lbl_ref = QLabel(f"{REFERENCE}")

        layout.addWidget(self.lbl_ref,3,2)

        #=========================================
        # Perturbación
        #=========================================

        layout.addWidget(QLabel("Perturbación [Nm]"),4,0)

        self.slider_dist = QSlider(Qt.Horizontal)

        self.slider_dist.setMinimum(int(DIST_MIN*1000))

        self.slider_dist.setMaximum(int(DIST_MAX*1000))

        self.slider_dist.setValue(int(DIST_AMPLITUDE*1000))

        layout.addWidget(self.slider_dist,4,1)

        self.lbl_dist = QLabel(f"{DIST_AMPLITUDE:.3f}")

        layout.addWidget(self.lbl_dist,4,2)

        #=========================================
        # Velocidad
        #=========================================

        layout.addWidget(QLabel("Velocidad"),5,0)

        self.slider_speed = QSlider(Qt.Horizontal)

        self.slider_speed.setMinimum(10)

        self.slider_speed.setMaximum(500)

        self.slider_speed.setValue(100)

        layout.addWidget(self.slider_speed,5,1)

        self.lbl_speed_slider = QLabel("1.0x")

        layout.addWidget(self.lbl_speed_slider,5,2)

        #=========================================
        # Eventos
        #=========================================

        self.slider_kp.valueChanged.connect(
            self.kp_changed
        )

        self.slider_ki.valueChanged.connect(
            self.ki_changed
        )

        self.slider_kd.valueChanged.connect(
            self.kd_changed
        )

        self.slider_ref.valueChanged.connect(
            self.reference_changed
        )

        self.slider_dist.valueChanged.connect(
            self.disturbance_changed
        )

        self.slider_speed.valueChanged.connect(
            self.speed_changed
        )

    #=========================================================
    # KP
    #=========================================================

    def kp_changed(self,value):

        kp = value/10000

        self.lbl_kp.setText(f"{kp:.4f}")

        self.sim.set_pid(
            kp,
            self.sim.ki,
            self.sim.kd
        )


    #=========================================================

    def ki_changed(self,value):

        ki = value/10000

        self.lbl_ki.setText(f"{ki:.4f}")

        self.sim.set_pid(
            self.sim.kp,
            ki,
            self.sim.kd
        )


    #=========================================================

    def kd_changed(self,value):

        kd = value/10000

        self.lbl_kd.setText(f"{kd:.4f}")

        self.sim.set_pid(
            self.sim.kp,
            self.sim.ki,
            kd
        )


    #=========================================================

    def reference_changed(self,value):

        self.lbl_ref.setText(f"{value}°")

        self.sim.set_reference(value)


    #=========================================================

    def disturbance_changed(self,value):

        amp = value/1000

        self.lbl_dist.setText(f"{amp:.3f}")

        self.sim.set_disturbance_amplitude(
            amp
        )


    #=========================================================

    def speed_changed(self,value):

        speed = value/100

        self.lbl_speed_slider.setText(
            f"{speed:.2f}x"
        )

        self.sim.simulation_speed = speed

    def create_buttons(self):

        frame = QFrame()

        layout = QHBoxLayout()

        frame.setLayout(layout)

        self.left_panel.addWidget(frame)

        #=========================================
        # Play / Pause
        #=========================================

        self.btn_play = QPushButton("⏸ Pausa")

        self.btn_play.setMinimumHeight(35)

        layout.addWidget(self.btn_play)

        #=========================================
        # Reset
        #=========================================

        self.btn_reset = QPushButton("Reset")

        self.btn_reset.setMinimumHeight(35)

        layout.addWidget(self.btn_reset)

        #=========================================
        # Ráfaga
        #=========================================

        self.btn_gust = QPushButton("Ráfaga")

        self.btn_gust.setMinimumHeight(35)

        layout.addWidget(self.btn_gust)

        #=========================================
        # Viento
        #=========================================

        self.btn_wind = QPushButton("Viento")

        self.btn_wind.setMinimumHeight(35)

        layout.addWidget(self.btn_wind)

        #=========================================
        # Turbulencia
        #=========================================

        self.btn_turb = QPushButton("Turbulencia")

        self.btn_turb.setMinimumHeight(35)

        layout.addWidget(self.btn_turb)

        layout.addStretch()

        #=========================================
        # Eventos
        #=========================================

        self.btn_play.clicked.connect(
            self.toggle_play
        )

        self.btn_reset.clicked.connect(
            self.reset_simulation
        )

        self.btn_gust.clicked.connect(
            self.gust_clicked
        )

        self.btn_wind.clicked.connect(
            self.wind_clicked
        )

        self.btn_turb.clicked.connect(
            self.turbulence_clicked
        )

    def toggle_play(self):

        if self.sim.running:

            self.sim.pause()

            self.btn_play.setText("▶ Play")

        else:

            self.sim.play()

            self.btn_play.setText("⏸ Pausa")

    def reset_simulation(self):

        self.sim.reset()

        self.btn_play.setText("⏸ Pausa")

    def gust_clicked(self):

        self.sim.enable_gust()


    def wind_clicked(self):

        self.sim.enable_wind()

        if self.sim.wind_active:

            self.btn_wind.setStyleSheet(
                "background-color: lightgreen;"
            )

        else:

            self.btn_wind.setStyleSheet("")

    def turbulence_clicked(self):

        self.sim.enable_turbulence()

        if self.sim.turbulence_active:

            self.btn_turb.setStyleSheet(
                "background-color: lightgreen;"
            )

        else:

            self.btn_turb.setStyleSheet("")

    def update_simulation(self):

        #-----------------------------------------
        # Avanzar simulación
        #-----------------------------------------
        try:

            if self.sim.running:

                n_steps = max(
                    1,
                    int(self.sim.simulation_speed * UPDATE_INTERVAL / (self.sim.dt * 1000))
                )

                for _ in range(n_steps):

                    self.sim.step()

            #-----------------------------------------
            # Obtener datos
            #-----------------------------------------

            data = self.sim.get_data()

            #-----------------------------------------
            # Actualizar gráficos
            #-----------------------------------------

            self.update_plots(data)

            #-----------------------------------------
            # Actualizar indicadores
            #-----------------------------------------

            self.update_indicators(data)

            #-----------------------------------------
            # Redibujar
            #-----------------------------------------

            self.canvas.draw_idle()

            #---------------------------------
            # FPS
            #---------------------------------

            self.frame_counter += 1

            now = time.time()

            elapsed = now - self.last_frame

            if elapsed >= 1:

                self.fps = self.frame_counter / elapsed

                self.frame_counter = 0

                self.last_frame = now
                
            self.btn_gust.setStyleSheet(
                "background-color: orange;" if self.sim.gust_active else ""
            )

            self.btn_wind.setStyleSheet(
                "background-color: lightgreen;" if self.sim.wind_active else ""
            )

            self.btn_turb.setStyleSheet(
                "background-color: lightblue;" if self.sim.turbulence_active else ""
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.timer.stop()

    def update_plots(self, data):

        t = data["time"]

        if len(t) == 0:
            return

        roll = data["roll"]

        error = data["error"]

        torque = data["torque"]

        disturbance = data["disturbance"]

        #---------------------------------
        # Roll
        #---------------------------------

        self.line_roll.set_data(t, roll)

        #---------------------------------
        # Error
        #---------------------------------

        self.line_error.set_data(t, error)

        #---------------------------------
        # Torque
        #---------------------------------

        self.line_torque.set_data(t, torque)

        #---------------------------------
        # Perturbación
        #---------------------------------

        self.line_dist.set_data(t, disturbance)

        #---------------------------------
        # Ventana deslizante
        #---------------------------------

        window = WINDOW_TIME

        xmax = max(window, t[-1])

        xmin = xmax - window

        for ax in (
            self.ax_roll,
            self.ax_error,
            self.ax_torque,
            self.ax_dist,
        ):

            ax.set_xlim(xmin, xmax)

        #---------------------------------
        # Autoscale vertical
        #---------------------------------

        for ax in (
            self.ax_roll,
            self.ax_error,
            self.ax_torque,
            self.ax_dist,
        ):

            ax.relim()

            ax.autoscale_view(
                scalex=False,
                scaley=True
            )

    def update_indicators(self, data):

        self.lbl_time.setText(
            f"Tiempo: {data['current_time']:.2f} s"
        )

        self.lbl_roll.setText(
            f"Roll: {np.degrees(data['current_roll']):6.2f} °"
        )

        self.lbl_error.setText(
            f"Error: {np.degrees(data['current_error']):6.2f} °"
        )

        self.lbl_torque.setText(
            f"Torque: {data['current_torque']:.4f} Nm"
        )

        self.lbl_imu.setText(
            f"IMU: {np.degrees(data['current_imu']):6.2f} °"
        )

        self.lbl_speed.setText(
            f"Velocidad angular: {np.degrees(data['current_speed']):6.2f} °/s"
        )

        self.lbl_acc.setText(
            f"Aceleración: {np.degrees(data['current_acc']):6.2f} °/s²"
        )

        self.lbl_state.setText(
            f"Estado: {data['current_state']}"
        )

        if self.sim.running:

            self.lbl_state.setStyleSheet(
                "color: green; font-weight: bold;"
            )

        else:

            self.lbl_state.setStyleSheet(
                "color: red; font-weight: bold;"
            )

    def create_statusbar(self):

        self.status = QStatusBar()

        self.left_panel.addWidget(self.status)

        self.status.showMessage(
            "Inicializando simulador..."
        )
    
