import numpy as np
import math


#5 1 2
#1 4 1
#2 1 3

# 2.2  1  0.5  2
# 1   1.3  2  1
# 0.5 2  0.5 1.6
# 2    1 1.6   2


def vector_norm(vector_x):
    norm = 0.0
    for i in range(len(vector_x)):
        norm += (vector_x[i] * vector_x[i])

    return math.sqrt(norm)


def power_iteration(matrix_a, epsilon, vector_x_0=None):
    n, _ = matrix_a.shape
    iteration = 0

    vector_x = vector_x_0 if vector_x_0 is not None else np.ones(n)
    p = np.dot(matrix_a, vector_x)
    eigenvalue = np.dot(p, vector_x)
    for k in range(1000):
        p = np.dot(matrix_a, vector_x)

        vector_x = p / vector_norm(p)
        new_eigenvalue = np.dot(p, vector_x)

        iteration += 1

        delta = abs(new_eigenvalue - eigenvalue)

        eigenvalue = new_eigenvalue

        if delta < epsilon:
            break

    return eigenvalue, vector_x, iteration


def deflate_matrix(matrix_a, eigenvalue, eigenvector):
    outer_product = np.outer(eigenvector, eigenvector)
    return matrix_a - eigenvalue * outer_product


def power_iteration_method(matrix_a, epsilon):
    eigenvalues = []
    iteration_list = []
    n, _ = matrix_a.shape
    matrix_a_copy = matrix_a.copy()

    for _ in range(n):
        eigenvalue, eigenvector, iteration = power_iteration(matrix_a_copy, epsilon)
        eigenvalues.append(eigenvalue)
        iteration_list.append(iteration)
        matrix_a_copy = deflate_matrix(matrix_a_copy, eigenvalue, eigenvector)

    return list(eigenvalues), iteration_list


def rotation_method(matrix_a, epsilon):
    n, _ = matrix_a.shape
    iteration = 0

    for k in range(1000):
        max_val = 0.0
        p, q = 0, 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(matrix_a[i, j]) > max_val:
                    max_val = abs(matrix_a[i, j])
                    p, q = i, j

        if max_val < epsilon:
            break

        if matrix_a[p, p] == matrix_a[q, q]:
            theta = np.pi / 4
        else:
            theta = np.arctan2(2 * matrix_a[p, q], matrix_a[p, p] - matrix_a[q, q]) / 2

        c, s = np.cos(theta), np.sin(theta)

        rotation_matrix = np.eye(n)
        rotation_matrix[p, p] = c
        rotation_matrix[q, q] = c
        rotation_matrix[p, q] = -s
        rotation_matrix[q, p] = s

        p = np.dot(rotation_matrix.T, matrix_a)
        matrix_a = np.dot(p, rotation_matrix)

        iteration += 1

    eigenvalues = np.diag(matrix_a)

    return list(eigenvalues), iteration



