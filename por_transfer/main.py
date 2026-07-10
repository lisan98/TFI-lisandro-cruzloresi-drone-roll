import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

from config import *

#----------------------------------
# Planta
#----------------------------------

G = ctrl.tf([1],[J,0,0])

#----------------------------------
# PID
#----------------------------------

C = ctrl.tf(
    [KD,KP,KI],
    [1,0]
)

#----------------------------------
# Sistema cerrado
#----------------------------------

H = ctrl.tf([1], [0.01, 1])

T = ctrl.feedback(C * G, H)

Td = ctrl.minreal(G / (1 + C * G * H))
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
#dist[(t>=2)&(t<=2.2)] = 0.002

#cambio de direccion del viento
#dist += 0.001*(0.5*t-0.5)*(t>2)*(t<5)

# turbulencia
dist += 0.003*np.sin(6*t)*(t>4)*(t<8)

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

plt.plot(
    t,
    np.degrees(y_total),
    label="Roll"
)

plt.grid()

plt.legend()

plt.subplot(212)

plt.plot(
    t,
    dist,
    label="Perturbación"
)

plt.grid()

plt.legend()

plt.show()