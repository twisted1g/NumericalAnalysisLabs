import re
import math

global_context = {
    'cos': math.cos,
    'sin': math.sin,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'exp': math.exp,
    'log': math.log,
    'pi': math.pi,
    'e': math.e,
    'abs': abs
}


def calculate_function(function_string, x, y):
    return eval(function_string, {"__builtins__": None, 'x': x, "y": y}, global_context)


def get_start_condition(condition):
    condition = re.split(r'[^\d.]', condition)
    while condition.count(''):
        condition.remove('')

    return float(condition[0]), float(condition[1])


#явный метод Эйлера
def forward_euler_method(function_string, start_condition, upper_limit, step):
    iteration = 0
    x_k, y_k = get_start_condition(start_condition)
    y_points = [y_k]
    x_points = [x_k]
    for _ in range(10000):
        y_k += step * calculate_function(function_string, x_k, y_k)
        x_k += step

        iteration += 1
        y_points.append(y_k)
        x_points.append(x_k)

        if x_k > upper_limit:
            break

    return iteration, x_points, y_points


def second_runge_kutta_method(function_string, start_condition, upper_limit, step):
    iteration = 0
    x_k, y_k = get_start_condition(start_condition)
    y_points = [y_k]
    x_points = [x_k]
    for _ in range(10000):
        k_1 = step * calculate_function(function_string, x_k, y_k)
        x_k += step
        k_2 = step * calculate_function(function_string, x_k, y_k + k_1)

        y_k += 0.5 * (k_1 + k_2)

        iteration += 1
        y_points.append(y_k)
        x_points.append(x_k)

        if x_k > upper_limit:
            break

    return iteration, x_points, y_points


def fourth_runge_kutta_method(function_string, start_condition, upper_limit, step):
    iteration = 0
    x_k, y_k = get_start_condition(start_condition)
    y_points = [y_k]
    x_points = [x_k]
    for _ in range(10000):
        k_1 = step * calculate_function(function_string, x_k, y_k)
        k_2 = step * calculate_function(function_string, x_k + step/2, y_k + k_1/2)
        k_3 = step * calculate_function(function_string, x_k + step/2, y_k + k_2/2)
        x_k += step
        k_4 = step * calculate_function(function_string, x_k, y_k + k_3)

        y_k += 1/6 * (k_1 + 2*k_2 + 2*k_3 + k_4)

        iteration += 1
        y_points.append(y_k)
        x_points.append(x_k)

        if x_k > upper_limit:
            break

    return iteration, x_points, y_points


def forward_forth_adams_method(function_string, start_condition, upper_limit, step):
    iteration = 0
    i, x, y = fourth_runge_kutta_method(function_string, start_condition, step * 2, step)
    iteration += i
    y_k = y[3]
    y_points = y.copy()
    x_points = x.copy()

    for _ in range(10000):
        x_k = x[-1]
        if x_k > upper_limit:
            break

        y_k += step/24 * (55 * calculate_function(function_string, x[3], y[3]) -
                                       59 * calculate_function(function_string, x[2], y[2]) +
                                       37 * calculate_function(function_string, x[1], y[1]) -
                                       9 * calculate_function(function_string, x[0], y[0]))

        x = [i + step for i in x]
        x_k = x[-1]
        for i in range(len(y)-1):
            y[i] = y[i+1]
        y[-1] = y_k

        iteration += 1
        y_points.append(y_k)
        x_points.append(x_k)

    return iteration, x_points, y_points


def not_forward_second_adams_method(function_string, start_condition, upper_limit, step):
    iteration = 0
    x_0, y_0 = get_start_condition(start_condition)
    y_points = [y_0]
    x_points = [x_0]
    for _ in range(10000):
        y_1 = y_0 + step * calculate_function(function_string, x_0, y_0)
        x_1 = x_0 + step

        new_y_1 = y_0 + step * 0.5 * (calculate_function(function_string, x_1, y_1) +
                                      calculate_function(function_string, x_0, y_0))

        while abs(new_y_1 - y_1) > 0.000001:
            iteration += 1
            y_1 = new_y_1
            new_y_1 = y_0 + step * 0.5 * (calculate_function(function_string, x_1, y_1) +
                                          calculate_function(function_string, x_0, y_0))

        y_1 = new_y_1
        y_0 = y_1
        x_0 = x_1
        iteration += 1
        y_points.append(y_1)
        x_points.append(x_1)

        if x_1 > upper_limit:
            break

    return iteration, x_points, y_points


#not_forward_second_adams_method("y+x", "y(0)=0", 1, 0.001)
