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

#(x - 1)*(x - 2)**2*(x - 3)**3


def calculate_function(function_string, x):
    return eval(function_string, {"__builtins__": None, 'x': x}, global_context)


def bisection_method(function, lower, upper, epsilon):
    if calculate_function(function, lower) * calculate_function(function, upper) >= 0:
        return None

    iteration = 0
    while abs(upper - lower) / 2.0 > epsilon:
        midpoint = (lower + upper) / 2.0
        if calculate_function(function, midpoint) == 0:
            return midpoint, iteration
        elif calculate_function(function, lower) * calculate_function(function, midpoint) < 0:
            upper = midpoint
        else:
            lower = midpoint
        iteration += 1

    return (lower + upper) / 2.0, iteration


def secant_method(function, x_0, x_1, epsilon):
    for iteration in range(1000):
        f_0 = calculate_function(function, x_0)
        f_1 = calculate_function(function, x_1)

        x_2 = x_1 - f_1 * (x_1 - x_0) / (f_1 - f_0)

        if abs(x_2 - x_1) < epsilon:
            return x_2, iteration

        x_0, x_1 = x_1, x_2
    return None


def newton_method(x_0, epsilon):

    def function(x):
        return x ** 3 - x - 2  # 1.52137

    def derivative(x):
        return 3 * x ** 2 - 1

    for iteration in range(1000):
        f_0 = function(x_0)
        df_0 = derivative(x_0)

        if df_0 == 0:
            return None

        x_1 = x_0 - f_0 / df_0

        if abs(x_1 - x_0) < epsilon:
            return x_1, iteration

        x_0 = x_1
    return None


def simple_iteration_method(x_0, epsilon, a):
    #x**2 - 2 = 0
    #x = 2/x
    def f(x):
        return a/x

    x = x_0
    for iteration in range(1000):
        x_next = 0.5*(x + f(x))
        if abs(x_next - x) < epsilon:
            return x_next, iteration + 1
        x = x_next
    return None


# print(bisection_method("(x - 1)*(x - 2)**2*(x - 3)**3", 0.59,  1.51, 0.000001))
# print(secant_method("(x - 1)*(x - 2)**2*(x - 3)**3", 0.1,  0.3, 0.000001))
# print(newton_method(1, 0.0001))
# print(simple_iteration_method(10, 0.000001, 2))
