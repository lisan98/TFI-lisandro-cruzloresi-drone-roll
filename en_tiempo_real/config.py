

# ==========================================================
# PARÁMETROS FÍSICOS DEL DRON
# ==========================================================

# Momento de inercia alrededor del eje Roll [kg·m²]
J = 1.14e-4

# ==========================================================
# MODELO DEL ESC
# ==========================================================

# Constante de tiempo del ESC [s]
TAU_ESC = 0.02

# Torque máximo que puede generar el conjunto motor + hélice
# (aproximado para un dron similar al DJI Mini 2)
MAX_TORQUE = 0.06      # [Nm]

# ==========================================================
# MODELO DEL IMU (MPU6050)
# ==========================================================

# Constante de tiempo del filtro del sensor
TAU_IMU = 0.01

# ==========================================================
# CONTROLADOR PID
# ==========================================================

KP = 0.0576
KI = 0.216
KD = 0.00768

# ==========================================================
# REFERENCIA
# ==========================================================

# Ángulo inicial de referencia [grados]
REFERENCE = 0

# ==========================================================
# SIMULACIÓN
# ==========================================================

# Paso de integración
DT = 0.001          # 1 ms (1000 Hz)

# Cantidad máxima de puntos mostrados
MAX_POINTS = 10000

# ==========================================================
# VELOCIDAD DE LA SIMULACIÓN
# ==========================================================

# Multiplicador de velocidad
SIMULATION_SPEED = 1.0

# ==========================================================
# PERTURBACIONES
# ==========================================================

# Amplitud inicial del torque perturbador
DIST_AMPLITUDE = 0.02      # Nm

# Duración de la ráfaga
GUST_DURATION = 0.20       # s

# Frecuencia de la turbulencia
TURB_FREQUENCY = 6.0       # Hz

# ==========================================================
# DASHBOARD
# ==========================================================

# Período de refresco de la interfaz
UPDATE_INTERVAL = 10       # ms

# ==========================================================
# LÍMITES DE LOS SLIDERS
# ==========================================================

KP_MIN = 0.0
KP_MAX = 0.20

KI_MIN = 0.0
KI_MAX = 1.00

KD_MIN = 0.0
KD_MAX = 0.05

DIST_MIN = 0.0
DIST_MAX = 0.05

# ==========================================================
# APARIENCIA DE LOS GRÁFICOS
# ==========================================================

WINDOW_TIME = 10.0     # segundos visibles

ROLL_YMIN = -45
ROLL_YMAX = 45

ERROR_YMIN = -45
ERROR_YMAX = 45

TORQUE_YMIN = -0.08
TORQUE_YMAX = 0.08

DIST_YMIN = -0.05
DIST_YMAX = 0.05