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


def calculate_function(func_string, x):
    return eval(func_string, {"__builtins__": None, 'x': x}, global_context)


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


def divided_differences(x, y):
    n = len(x)
    table = [y.copy()]
    for j in range(1, n):
        row = []
        for i in range(n - j):
            diff = (table[j - 1][i + 1] - table[j - 1][i]) / (x[i + j] - x[i])
            row.append(diff)
        table.append(row)
    return table


def newton_polynomial(x, y, x_value):
    table = divided_differences(x, y)
    n = len(x)
    result = table[0][0]
    omega = 1
    for i in range(1, n):
        omega *= (x_value - x[i - 1])
        result += table[i][0] * omega
    return result


def get_newton_polynomial(x_points, x_interpolation, y_interpolation):
    y_points = []
    for x in x_points:
        res = newton_polynomial(x_interpolation, y_interpolation, x)
        y_points.append(res)

    return y_points

