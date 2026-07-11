import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

from config import *

#----------------------------------
# Proceso
#----------------------------------

G = ctrl.tf([1],[J,0,0])

#----------------------------------
# ESC
#----------------------------------

ESC = ctrl.tf(
    [1],
    [TAU_ESC,1]
)

#----------------------------------
# PID
#----------------------------------

C = ctrl.tf(
    [KD,KP,KI],
    [1,0]
)

#----------------------------------
# Elemento de medicion IMU(Giroscopio)
#----------------------------------

H = ctrl.tf([1], [TAU_IMU, 1])

#----------------------------------
# Sistema cerrado
#----------------------------------


T = ctrl.feedback(C * ESC * G, H)

Td = ctrl.minreal(G / (1 + C * G * H * ESC))
#----------------------------------

t = np.arange(
    0,
    TIME,
    DT
)

# referencia

r = np.zeros_like(t)

r[t>=0]=np.deg2rad(0)

#----------------------------------

resp = ctrl.forced_response(T, t, r)

tout = resp.time
y = resp.outputs

#----------------------------------
# Perturbaciones
#----------------------------------

dist = np.zeros_like(t)

#rafaga
dist[(t>=2)&(t<=2.2)] = 0.02

#cambio de direccion del viento
dist += 0.01*(0.5*t-0.5)*(t>4)*(t<6)

# turbulencia
dist += 0.03*np.sin(6*t)*(t>8)*(t<10)

resp_d = ctrl.forced_response(Td, t, dist)

yd = resp_d.outputs

#----------------------------------
# Salida total
#----------------------------------

y_total = y + yd

print("KP =", KP)
print("KI =", KI)
print("KD =", KD)

print(C)

print(T)

print(Td)

print(ctrl.poles(T))
print(ctrl.poles(Td))

plt.figure(figsize=(12,7))

plt.subplot(211)

plt.plot(t, np.degrees(y_total), label="Roll")

plt.xlabel("Tiempo [s]")
plt.ylabel("Ángulo de roll [°]")

plt.grid()

plt.legend()

plt.subplot(212)

plt.plot(
    t,
    dist,
    label="Perturbación"
)
plt.xlabel("Tiempo [s]")
plt.ylabel("Torque [Nm]")
plt.grid()

plt.legend()

plt.show()



