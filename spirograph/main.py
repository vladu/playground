import collections
import warnings

import numpy
import turtle as turtle_mod


def _draw_curve_async(points):
    turtle = turtle_mod.Turtle()

    p0 = None

    for idx, p in enumerate(points):
        if idx == 0:
            turtle.penup()
            turtle.goto(p[0], p[1])
            p0 = p
            turtle.pendown()
        else:
            turtle.goto(p[0], p[1])
        yield idx

    if p0 is not None:
        turtle.goto(p0[0], p0[1])

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


def _num_revs(inner_r, outer_r):
    result = inner_r / numpy.gcd(inner_r, outer_r)
    print('For R={}, r={}, num_revs={}'.format(outer_r, inner_r, result))
    return result


def _calc_phis(inner_r, outer_r, rad_incr):
    return numpy.arange(0, 2 * numpy.pi * _num_revs(inner_r, outer_r), rad_incr)


def calc_spiro(x0, y0, outer_r, inner_r, pen_r_pct, rad_incr=0.05):
    k = inner_r / outer_r

    phi = _calc_phis(inner_r, outer_r, rad_incr)
    if len(phi) > 6000:
        print('Num-points for R={}, r={} is {} is too long...'.format(outer_r, inner_r, len(phi)))
        rad_incr *= 2
        phi = _calc_phis(inner_r, outer_r, rad_incr)
        print('Adjusted to {} points'.format(len(phi)))
    return numpy.asarray([
        x0 + outer_r * ((1 - k) * numpy.cos(phi) + pen_r_pct * k * numpy.cos(phi * (1 - k) / k)),
        y0 + outer_r * ((1 - k) * numpy.sin(phi) + pen_r_pct * k * numpy.sin(phi * (1 - k) / k)),
    ]).T


def calc_circle(x, y, r):
    phi = numpy.arange(0, 2 * numpy.pi, 0.05)
    return numpy.asarray([x + r * numpy.cos(phi), y + r * numpy.sin(phi)]).T


def calc_rand_spiro(window_w, window_h, outer_min=50, inner_min=10, k_max=0.6, l_min=0.1, l_max=0.9):
    outer_r = numpy.random.randint(outer_min, min(window_w, window_h) / 2)
    inner_r = numpy.random.randint(inner_min, k_max * outer_r)

    # Check if the two radii are mutually prime
    # If so, the number of loops is likely going to be so big, it's going to take forever to render
    # Then make both radii the adjacent even number, to cut the number of loops at least in half
    if _num_revs(inner_r, outer_r) == inner_r:
        print('Raddi R={} and r={} are mutually prime...'.format(outer_r, inner_r))
        if outer_r % 2 == 1:
            outer_r -= 1
        if inner_r % 2 == 1:
            inner_r -= 1
        print('Adjusted to R={}, r={}'.format(outer_r, inner_r))

    half_w = window_w / 2 - outer_r
    half_h = window_h / 2 - outer_r
    return dict(
        x0=numpy.random.randint(-half_w, half_w),
        y0=numpy.random.randint(-half_h, half_h),
        outer_r=outer_r,
        inner_r=inner_r,
        pen_r_pct=numpy.random.uniform(l_min, l_max),
    )


def main():
    # draw_curves([
    #     calc_circle(100, 100, 50),
    #     calc_spiro(50, 50, 220, 65, 0.8),
    # ])
    draw_curves(list(
        calc_spiro(**kwargs)
        for kwargs in (
            calc_rand_spiro(turtle_mod.window_width(), turtle_mod.window_height()) for
            _ in range(2)
        )
    ))
    turtle_mod.mainloop()


if __name__ == '__main__':
    main()
