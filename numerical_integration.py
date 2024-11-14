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


def calculate_function(function_string, x):
    return eval(function_string, {"__builtins__": None, 'x': x}, global_context)


def middle_rectangle_method(function_string, low_limit, high_limit, n):
    h = (high_limit - low_limit) / n
    area = 0.0

    for i in range(n):
        midpoint = low_limit + (i + 0.5) * h
        area += calculate_function(function_string, midpoint) * h

    return area


def simpson_method(function_string, low_limit, high_limit, n):
    h = (high_limit - low_limit) / n
    summa = 0.0

    x0 = low_limit
    x1 = low_limit + h

    for i in range(n):
        summa += (calculate_function(function_string, x0) + 4 * calculate_function(function_string, x0 + h / 2)
                  + calculate_function(function_string, x1))
        x0 += h
        x1 += h
    return (h / 6) * summa


def gauss_method_fourth_power(function_string, low_limit, high_limit):
    values_weight = [0.347854845, 0.652145155, 0.652145155, 0.347854845]
    values_args = [-0.8611363115940525, -0.33998104358485626, 0.33998104358485626, 0.8611363115940525]

    summa = 0.0
    for i in range(4):
        arg = 0.5 * (high_limit + low_limit) + 0.5 * (high_limit - low_limit) * values_args[i]
        summa += 0.5 * (high_limit - low_limit) * values_weight[i] * calculate_function(function_string, arg)

    return summa


def runge_rule(numerical_integration, epsilon, runge_coefficient, function_string, low_limit, high_limit):
    integral_n = 0
    n = 100
    integral_2n = numerical_integration(function_string, low_limit, high_limit, n)

    while runge_coefficient * abs(integral_n - integral_2n) >= epsilon:
        n *= 2
        integral_n = integral_2n
        s2 = numerical_integration(function_string, low_limit, high_limit, n)

    return integral_2n


def get_function_points_x(
        dots: int,
        start: float,
        end: float,
        k: int = 1
) -> list[float]:

    h: float = abs(end - start) / (dots * k)
    x = [start + i * h for i in range(dots * k + 1)]
    return x

def get_function_points_y(
        func_str: str,
        x: list[float]
) -> list[float]:
    y = [calculate_function(func_str, i) for i in x]
    return y
