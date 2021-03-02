import numpy
import turtle as turtle_mod


def draw_points(points):
    turtle = turtle_mod.Turtle()
    turtle.penup()
    turtle.goto(points[0][0], points[0][1])
    turtle.pendown()

    for p in points:
        turtle.goto(p[0], p[1])

    turtle.hideturtle()


def draw_spiro(x0, y0, outer_r, inner_r, pen_r_pct, rad_incr=0.05):
    k = inner_r / outer_r

    phi = numpy.arange(0, 2 * numpy.pi * inner_r / numpy.gcd(inner_r, outer_r), rad_incr)
    points = numpy.asarray([
        x0 + outer_r * ((1 - k) * numpy.cos(phi) + pen_r_pct * k * numpy.cos(phi * (1 - k) / k)),
        y0 + outer_r * ((1 - k) * numpy.sin(phi) + pen_r_pct * k * numpy.sin(phi * (1 - k) / k)),
    ]).T
    draw_points(points)


def draw_circle(x, y, r):
    phi = numpy.arange(0, 2 * numpy.pi, 0.05)
    points = numpy.asarray([x + r * numpy.cos(phi), y + r * numpy.sin(phi)]).T
    draw_points(points)


def main():
    draw_circle(100, 100, 50)
    draw_spiro(50, 50, 220, 65, 0.8)
    turtle_mod.mainloop()


if __name__ == '__main__':
    main()
