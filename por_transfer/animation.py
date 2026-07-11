import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg
from matplotlib.transforms import Affine2D

# -------------------------------
# Imagen del drone
# -------------------------------




def animate_roll(t, roll, dist):

    fig, ax = plt.subplots(figsize=(8,6))

    img = mpimg.imread(
    r"C:\Users\lisan\Desktop\Lisandro\TdC\TFI-lisandro-cruzloresi-drone-roll\por_transfer\drone.png"
    )

    image = ax.imshow(
        img,
        extent=(-0.15, 0.15, -0.08, 0.08),
        zorder=5
    )

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

        trans = (
            Affine2D()
            .rotate_around(0, 0, phi)
            + ax.transData
        )

        image.set_transform(trans)
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

        return image, text, wind

    STEP = 10

    ani = FuncAnimation(
        fig,
        update,
        frames=range(0, len(t), STEP),
        interval=10,
        blit=False
    )

    plt.show()