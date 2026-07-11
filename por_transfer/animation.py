import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate_roll(t, roll, dist):

    fig, ax = plt.subplots(figsize=(8,6))

    ax.set_xlim(-0.35,0.35)
    ax.set_ylim(-0.25,0.25)
    ax.set_aspect("equal")

    ax.set_title("Simulación del Control de Roll")

    # Horizonte
    ax.plot(
        [-0.4,0.4],
        [0,0],
        '--',
        color="gray",
        linewidth=1
    )

    # Barra del drone
    drone, = ax.plot([],[],
                     linewidth=5,
                     color="black")

    # Motores
    motor1, = ax.plot([],[],
                      'bo',
                      markersize=12)

    motor2, = ax.plot([],[],
                      'bo',
                      markersize=12)

    # Flecha del viento
    wind = ax.arrow(
        0,
        0,
        0,
        0,
        color="red"
    )

    text = ax.text(
        -0.33,
        0.20,
        ""
    )

    L = 0.15

    def update(i):

        nonlocal wind

        wind.remove()

        phi = roll[i]

        x1 = -L*np.cos(phi)
        y1 = -L*np.sin(phi)

        x2 = L*np.cos(phi)
        y2 = L*np.sin(phi)

        drone.set_data(
            [x1,x2],
            [y1,y2]
        )

        motor1.set_data(
            [x1],
            [y1]
        )

        motor2.set_data(
            [x2],
            [y2]
        )

        if abs(dist[i]) > 1e-8:

            wind = ax.arrow(
                0.27,
                0.12,
                -0.12,
                0,
                width=0.005,
                color="red"
            )

        else:

            wind = ax.arrow(
                0,
                0,
                0,
                0,
                alpha=0
            )

        text.set_text(
            f"Tiempo : {t[i]:.2f} s\n"
            f"Roll : {np.degrees(phi):.2f}°"
        )

        return drone,motor1,motor2,text,wind

    STEP = 10

    ani = FuncAnimation(
        fig,
        update,
        frames=range(0, len(t), STEP),
        interval=10,
        blit=False
    )

    plt.show()