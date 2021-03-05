from importlib import resources as pkg_resources

import numpy
from matplotlib import animation
from matplotlib import colors as mpc
from matplotlib import pyplot as plt
from scipy import ndimage

from conway import structures


def calc_next_board(board):
    filt_board = (ndimage.uniform_filter(board, size=3, mode='wrap') * 9).round()

    # Starting from:
    # 0: 3 -> 1, else 0
    # 1: 3 or 4 -> 1 else 0
    next_board = numpy.where(board == 0, filt_board == 3, numpy.isin(filt_board, (3, 4))).astype(float)

    return next_board


def animate_board(board, generations=10, interval=50):
    fig = plt.figure()
    cmap = mpc.ListedColormap(['black', 'tan'])
    img = plt.imshow(board, cmap=cmap)
    plt.axis('off')
    plt.tight_layout(pad=0.)
    fig.patch.set_facecolor('dimgrey')

    def _animate(idx):
        next_board = calc_next_board(board)
        img.set_data(calc_next_board(board))
        board[:] = next_board[:]
        return img,

    _ = animation.FuncAnimation(fig, _animate, frames=generations, interval=interval, blit=True)
    plt.show()


def read_structure(name):
    with pkg_resources.path(structures, '{}.txt'.format(name)) as p:
        return numpy.loadtxt(p)


def add_structure(board, name, location):
    structure = read_structure(name)
    board[location[0]:location[0]+structure.shape[0], location[1]:location[1]+structure.shape[1]] = structure


def create_board(h=200, w=300):
    board = numpy.zeros((h, w))
    add_structure(board, 'r_pentomino', (65, 145))
    return board


def main():
    animate_board(create_board())


if __name__ == '__main__':
    main()
