import collections

import numpy
import turtle as turtle_mod


def _draw_curve_async(points):
    turtle = turtle_mod.Turtle()

    for idx, p in enumerate(points):
        if idx == 0:
            turtle.penup()
            turtle.goto(p[0], p[1])
            turtle.pendown()
        else:
            turtle.goto(p[0], p[1])
        yield idx

    turtle.hideturtle()


def draw_curve(points):
    cnt = 0
    for cnt in _draw_curve_async(points):
        pass
    return cnt


def draw_curves(curves, t=10):
    all_gens = collections.OrderedDict((_draw_curve_async(points), 0) for points in curves)
    done_gens = set()

    def one_step():
        if len(done_gens) < len(all_gens):
            for gen in all_gens.keys():
                if gen not in done_gens:
                    try:
                        all_gens[gen] = next(gen)
                    except StopIteration:
                        done_gens.add(gen)
            turtle_mod.ontimer(one_step, t)

    turtle_mod.ontimer(one_step, t)


def calc_spiro(x0, y0, outer_r, inner_r, pen_r_pct, rad_incr=0.05):
    k = inner_r / outer_r

    phi = numpy.arange(0, 2 * numpy.pi * inner_r / numpy.gcd(inner_r, outer_r), rad_incr)
    return numpy.asarray([
        x0 + outer_r * ((1 - k) * numpy.cos(phi) + pen_r_pct * k * numpy.cos(phi * (1 - k) / k)),
        y0 + outer_r * ((1 - k) * numpy.sin(phi) + pen_r_pct * k * numpy.sin(phi * (1 - k) / k)),
    ]).T


def calc_circle(x, y, r):
    phi = numpy.arange(0, 2 * numpy.pi, 0.05)
    return numpy.asarray([x + r * numpy.cos(phi), y + r * numpy.sin(phi)]).T


def main():
    draw_curves([
        calc_circle(100, 100, 50),
        calc_spiro(50, 50, 220, 65, 0.8),
    ])
    turtle_mod.mainloop()


if __name__ == '__main__':
    main()
