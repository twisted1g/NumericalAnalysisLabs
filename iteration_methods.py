import numpy as np
import math

#2 1 1
#1 3 2

#1 1 5
#3 -2 10


def vector_norm(vector_x):
    norm = 0.0
    for i in range(len(vector_x)):
        norm += (vector_x[i] * vector_x[i])

    return math.sqrt(norm)


def over_relaxation_method(matrix_a, vector_b, omega, epsilon, vector_x_0=None):
    n, _ = matrix_a.shape
    iteration = 0
    residual_list = []

    vector_x = vector_x_0 if vector_x_0 is not None else np.zeros(n)
    for k in range(1000):
        new_vector_x = np.copy(vector_x)
        for i in range(n):
            sum_ax = np.dot(matrix_a[i], new_vector_x) - matrix_a[i][i] * new_vector_x[i]
            new_vector_x[i] = (1 - omega) * vector_x[i] + (omega / matrix_a[i][i]) * (vector_b[i] - sum_ax)

        vector = new_vector_x - vector_x
        vector_x = new_vector_x
        iteration += 1
        residual_norm = vector_norm(find_residual_vector(vector_x, matrix_a, vector_b))
        residual_list.append(residual_norm)

        if vector_norm(vector) < epsilon:
            break

    return vector_x, residual_list, iteration


def seidel_method(matrix_a, vector_b, epsilon, vector_x_0=None):
    n, _ = matrix_a.shape
    iteration = 0
    residual_list = []

    vector_x = vector_x_0 if vector_x_0 is not None else np.zeros(n)
    for k in range(1000):
        new_vector_x = np.copy(vector_x)
        for i in range(n):
            sum1 = np.dot(matrix_a[i, :i], new_vector_x[:i])
            sum2 = np.dot(matrix_a[i, i + 1:], vector_x[i + 1:])
            new_vector_x[i] = (vector_b[i] - sum1 - sum2) / matrix_a[i, i]

        vector = new_vector_x - vector_x
        vector_x = new_vector_x
        iteration += 1
        residual_norm = vector_norm(find_residual_vector(vector_x, matrix_a, vector_b))
        residual_list.append(residual_norm)

        if vector_norm(vector) < epsilon:
            break

    return vector_x, residual_list, iteration


def steepest_descent_method(matrix_a, vector_b, epsilon, vector_x_0=None):
    n, _ = matrix_a.shape
    iteration = 0
    residual_list = []

    vector_x = vector_x_0 if vector_x_0 is not None else np.zeros(n, dtype=np.longdouble)
    residual_vector = np.dot(matrix_a, vector_x) - vector_b

    for k in range(1000):
        vector_p = np.dot(matrix_a, residual_vector)
        tau = (np.dot(residual_vector, residual_vector)) / (np.dot(vector_p, residual_vector))

        new_vector_x = vector_x - np.dot(tau, residual_vector)

        vector = new_vector_x - vector_x
        new_residual_vector = residual_vector
        residual_list.append(vector_norm(new_residual_vector))

        vector_x = new_vector_x
        residual_vector = np.dot(matrix_a, vector_x) - vector_b
        iteration += 1

        if vector_norm(vector) < epsilon:
            break

    return vector_x, residual_list, iteration


def find_residual_vector(vector_x, matrix_a, matrix_b):
    n, m = matrix_a.shape
    residual_vector = np.zeros(n)

    for i in range(n):
        for j in range(m):
            residual_vector[i] += matrix_a[i][j] * vector_x[j]
        residual_vector[i] -= matrix_b[i]
    residual_vector = np.asarray(residual_vector, dtype=np.longdouble)

    return residual_vector

