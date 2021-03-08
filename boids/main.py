import numpy
from matplotlib import animation
from matplotlib import pyplot as plt


def main(w=640, h=480, count=50, interval=50):
    pos = numpy.asarray([h / 2 + h / 20 * numpy.random.rand(count), w / 2 + w / 20 * numpy.random.rand(count)]).T
    rads = 2 * numpy.pi * numpy.random.rand(count)
    vels = numpy.asarray([numpy.sin(rads), numpy.cos(rads)]).T

    fig = plt.figure()
    plt.axis('off')
    plt.tight_layout(pad=0.)
    ax = plt.axes(xlim=(0, w), ylim=(0, h))
    bodies, = ax.plot([], [], markersize=10, c='k', marker='o', ls='None')
    beaks, = ax.plot([], [], markersize=4, c='r', marker='o', ls='None')

    def _update(idx):
        pos[:] = pos + vels

        bodies.set_data(pos[:,1 ], pos[:, 0])
        beaks.set_data((pos + vels)[:, 1], (pos + vels)[:, 0])

    anim = animation.FuncAnimation(fig, _update, interval=interval)
    plt.show()


if __name__ == '__main__':
    main()
