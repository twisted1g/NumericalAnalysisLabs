import numerical_integration as ni
import math


def fourier_series(function, dots, count, epsilon):
    step = 2*math.pi/dots
    x_points = [-math.pi+step*i for i in range(dots+1)]

    a_0 = ni.runge_rule(ni.gauss_method_fourth_power, epsilon, 1/15, function, -math.pi, math.pi)
    a_0 /= math.pi
    y_points = [a_0/2 for _ in x_points]

    for n in range(1, count + 1):
        a_n = ni.runge_rule(ni.gauss_method_fourth_power, epsilon, 1/15, f"({function})"+f"*cos({n}*x)", -math.pi, math.pi)
        a_n /= math.pi

        b_n = ni.runge_rule(ni.gauss_method_fourth_power, epsilon, 1 / 15, f"({function})" + f"*sin({n}*x)", -math.pi, math.pi)
        b_n /= math.pi
        print(a_n, b_n)
        for i in range(len(x_points)):
            y_points[i] += (a_n * math.cos(n*x_points[i]) + b_n * math.sin(n*x_points[i]))

    return x_points, y_points

# def fourier_series(function, dots, count, epsilon):
#     step = 2*math.pi/dots
#     x_points = [-math.pi+step*i for i in range(dots+1)]
#
#     a_0 = (1+math.pi**2/3)
#     y_points = [a_0 for _ in x_points]
#
#     for n in range(1, count + 1):
#         a_n = 4 * (-1)**n/n**2
#
#         print(a_n)
#         for i in range(len(x_points)):
#             y_points[i] += a_n * math.cos(n * x_points[i])
#
#     return x_points, y_points


#fourier_series("x**2+1", 10, 5, 0.000001)