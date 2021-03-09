import numpy
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy.spatial import distance as sdist


def initialize_data(w, h, count):
    pos = numpy.asarray([h / 2 + h / 20 * numpy.random.rand(count), w / 2 + w / 20 * numpy.random.rand(count)]).T
    rads = 2 * numpy.pi * numpy.random.rand(count)
    vels = numpy.asarray([numpy.sin(rads), numpy.cos(rads)]).T
    return pos, vels


def initialize_plots(w, h):
    fig = plt.figure()
    plt.axis('off')
    plt.tight_layout(pad=0.)
    ax = plt.axes(xlim=(0, w), ylim=(0, h))
    bodies, = ax.plot([], [], markersize=10, c='k', marker='o', ls='None')
    beaks, = ax.plot([], [], markersize=4, c='r', marker='o', ls='None')
    return fig, bodies, beaks


def limit(arr, val):
    return numpy.where(numpy.abs(arr) > val, numpy.sign(arr) * val, arr)


def update_vels(pos, vels, vel_max_incr, vel_max):
    dist = sdist.squareform(sdist.pdist(pos))

    # Separation
    too_close = dist < 25
    vel_incr1 = pos * too_close.sum(axis=1).reshape((pos.shape[0], 1)) - too_close.dot(pos)
    vel_incr1 = limit(vel_incr1, vel_max_incr)

    # Alignment
    align = dist < 50
    vel_incr2 = limit(align.dot(pos), vel_max_incr)

    # Cohesion
    vel_incr3 = limit(align.dot(pos) - pos, vel_max_incr)

    vels = vels + vel_incr1 + vel_incr2 + vel_incr3
    vels = limit(vels, vel_max)
    return vels


def update_positions(w, h, pos, vels):
    pos = pos + vels
    pos[:, 0] = numpy.where(pos[:, 0] < 0, h, numpy.where(pos[:, 0] > h, 0, pos[:, 0]))
    pos[:, 1] = numpy.where(pos[:, 1] < 0, w, numpy.where(pos[:, 1] > w, 0, pos[:, 1]))
    return pos


def scatter(x, y, pos, vels, vel_max):
    return limit(vels + 0.1 * (pos - [y, x]), vel_max)


def main(w=640, h=480, count=50, interval=50, vel_max_incr=0.03, vel_max=2):
    pos, vels = initialize_data(w, h, count)
    fig, bodies, beaks = initialize_plots(w, h)

    def _update(idx):
        vels[:] = update_vels(pos, vels, vel_max_incr, vel_max)
        pos[:] = update_positions(w, h, pos, vels)

        bodies.set_data(pos[:, 1], pos[:, 0])
        beaks.set_data((pos + vels)[:, 1], (pos + vels)[:, 0])

    anim = animation.FuncAnimation(fig, _update, interval=interval)

    def _onclick(event):
        if event.button == 3:
            vels[:] = scatter(event.xdata, event.ydata, pos, vels, vel_max)

    cid = fig.canvas.mpl_connect('button_press_event', _onclick)

    plt.show()


if __name__ == '__main__':
    main()
