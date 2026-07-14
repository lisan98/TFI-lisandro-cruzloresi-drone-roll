# TFI-lisandro-cruzloresi-drone-roll
En este repo se encuentra la simulacion realizada para el trabajo final integrador de Lisandro Cruz Loresi.
El trabajo consiste en el control del Roll de un drone cuadricoptero.

Hay 3 carpetas en el repositorio, cada una es un simulador por separado:
 - La carpeta estatico_con_drone_animado solo muestra el grafico estatico del torque de perturbacion y el angulo(salida).
 - La carpeta dashboard_fijo muestran los graficos estaticos de angulo(salida), torque del actuador, error y perturbaciones que se puede modificar sus caracteristicas en el momento permitiendo setear distinas perturbaciones y valores de las constantes del PID.
 - La carpeta en_tiempo_real muestra la version final de la simulacion donde se puede correr un tablero interactivo donde la simulacion corre en tiempo real con la posibilidad de modificar los parametros de la simulacion como las constantes del PID, amplitud de las perturbaciones, el valor de señal de referencia, velocidad de simulacion y ademas de poder frenarla, reanudarla o resetearla si es necesario. 

Para poder correr las simulaciones hay que ejecutar el main.py teniendo instaldas las libraries numpy, matplotlib, control y pyqt5.

