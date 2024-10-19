import math
import numpy as np

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

def lagrange_polynomial(
        x: float,
        func_x: list[float],
        func_y: list[float]
) -> float:
    summa: float = 0.0
    for i in range(len(func_x)):
        pol: float = 1.0
        for j in range(len(func_x)):
            if i != j:
                pol *= (x - func_x[j]) / (func_x[i] - func_x[j])
        summa += (pol * func_y[i])
    return summa

def get_interpolation_function(
        nodes_x: list[float],
        nodes_y: list[float],
        points_x
) -> list[float]:
    func_y = [lagrange_polynomial(x, nodes_x, nodes_y) for x in points_x]
    return func_y

def get_chebyshev_nodes(
        a: float,
        b: float,
        n: int

) -> list[float]:
    nodes = [
        0.5 * (a + b) + 0.5 * (b - a) * math.cos((2 * k - 1) * math.pi / (2 * n))
        for k in range(1, n + 1)
    ]
    return nodes

def spline_build_full_matrix_with_c_coefficient(
        h: float,
        func_y: list[float]
):
    dim = len(func_y) - 1
    matrix_c = np.zeros((dim+1, dim+1), dtype="float")
    vector_b = np.zeros(dim+1, dtype="float")

    matrix_c[0, 0] = 1
    vector_b[0] = 0
    for i in range(1, dim):
        matrix_c[i, i - 1] = h
        matrix_c[i, i] = 4 * h
        matrix_c[i, i + 1] = h
        vector_b[i] = 3 * ((func_y[i + 1] - func_y[i]) / h - (func_y[i] - func_y[i - 1]) / h)
    matrix_c[dim, dim] = 1
    vector_b[dim] = 0

    return matrix_c, vector_b


def spline_calculate_c_coefficient(
        h: float,
        func_y: list[float]
) -> list[float]:
    matrix_c, vector_b = spline_build_full_matrix_with_c_coefficient(h, func_y)
    vector_c = np.linalg.solve(matrix_c, vector_b)

    return list(vector_c)


def spline_calculate_d_coefficient(
        h: float,
        vector_c: list[float]
) -> list[float]:
    vector_d: list[float] = []
    for i in range(1, len(vector_c)):
        element: float = (vector_c[i] - vector_c[i-1]) / 3 * h
        vector_d.append(element)

    return vector_d

def spline_calculate_b_coefficient(
        h: float,
        vector_c: list[float],
        func_y: list[float]
) -> list[float]:
    vector_b: list[float] = []
    for i in range(1, len(vector_c)):
        element: float = (func_y[i] - func_y[i-1]) / h - (2 * vector_c[i-1] + vector_c[i]) / 3
        vector_b.append(element)

    return vector_b

def calculate_spline(
        func_x: list[float],
        vector_a: list[float],
        vector_b: list[float],
        vector_c: list[float],
        vector_d: list[float],
        dot_count: int = 2
) -> tuple[list[float], list[float]]:
    spline_y: list[float] = []
    spline_x: list[float] = []


    for i in range(len(vector_c)):
        h = abs(func_x[i] - func_x[i+1]) / dot_count
        x = func_x[i]
        while x <= func_x[i+1]:
            spline: float = (vector_a[i] + vector_b[i] * (x - func_x[i+1]) + vector_c[i] * (x - func_x[i+1]) ** 2
                             + vector_d[i] * (x - func_x[i+1]) ** 3)

            spline_x.append(x)
            spline_y.append(spline)
            x += h

    return spline_x, spline_y


