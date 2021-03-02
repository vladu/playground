import math
import turtle


def draw_points(x0, y0, points):
    turtle.penup()
    turtle.goto(x0, y0)
    turtle.pendown()

    for p in points:
        turtle.goto(p[0], p[1])


def draw_circle(x, y, r):
    points = (
        (x + r * math.cos(rad), y + r * math.sin(rad))
        for rad in (math.radians(deg) for deg in range(0, 365, 1))
    )
    draw_points(x + r, y, points)


def main():
    draw_circle(100, 100, 50)
    turtle.mainloop()


if __name__ == '__main__':
    main()
