import numpy
import turtle


def draw_points(x0, y0, points):
    turtle.penup()
    turtle.goto(x0, y0)
    turtle.pendown()

    for p in points:
        turtle.goto(p[0], p[1])


def draw_circle(x, y, r):
    phi = numpy.arange(0, 2 * numpy.pi, 0.05)
    points = numpy.asarray([x + r * numpy.cos(phi), y + r * numpy.sin(phi)]).T
    draw_points(x + r, y, points)


def main():
    draw_circle(100, 100, 50)
    turtle.mainloop()


if __name__ == '__main__':
    main()
