import numpy as np

def make_identity(matrix):
    for current_row_index in range(len(matrix) - 1, 0, -1):
        current_row = matrix[current_row_index]
        for above_row in matrix[:current_row_index]:
            multiplier = above_row[current_row_index]
            above_row -= multiplier * current_row


def gauss_func(matrix):
    for row_index in range(len(matrix)):
        pivot_index = row_index + np.argmax(abs(matrix[row_index:, row_index]))
        if pivot_index != row_index:
            matrix[[row_index, pivot_index]] = matrix[[pivot_index, row_index]]

        current_row = matrix[row_index]
        pivot_value = current_row[row_index]

        if abs(pivot_value) < 1e-10:
            raise ValueError("Матрица несовместна")

        current_row /= pivot_value

        for lowerRow in matrix[row_index + 1:]:
            factor = lowerRow[row_index]
            lowerRow -= factor * current_row

    make_identity(matrix)


def write_gauss_answer(matrix):
    n, m = matrix.shape
    vector_x = []
    answer = ""
    for i in range(n):
        if any(matrix[i][j] != 0 for j in range(m - 1) if j != i):
            return "Система неоднородна"
        answer += f"x_{i} = {matrix[i][m - 1]}\n"
        vector_x.append(matrix[i][m - 1])

    vector_x = np.asarray(vector_x, dtype=np.longdouble)

    return answer, vector_x


def find_vector(vector_x, matrix_a, matrix_b):
    residual_vector = []
    n, m = matrix_a.shape
    for i in range(n):
        residual_vector.append(0)

    for i in range(n):
        for j in range(m):
            residual_vector[i] += matrix_a[i][j] * vector_x[j]
        residual_vector[i] -= matrix_b[i]
    residual_vector = np.asarray(residual_vector, dtype=np.longdouble)

    return residual_vector


def get_diagonal(matrix_a):
    n, m = matrix_a.shape
    if (n != m):
        raise ValueError("Матрица не тридиагональная")

    upper_diagonal = []
    diagonal = []
    lower_diagonal = []

    for i in range(n):
        for j in range(m):
            if i == j:
                diagonal.append(matrix_a[i][j])
            elif i == j - 1:
                upper_diagonal.append(matrix_a[i][j])
            elif i == j + 1:
                lower_diagonal.append(matrix_a[i][j])

    lower_diagonal = np.asarray(lower_diagonal, dtype=np.longdouble)
    diagonal = np.asarray(diagonal, dtype=np.longdouble)
    upper_diagonal = np.asarray(upper_diagonal, dtype=np.longdouble)

    return lower_diagonal, diagonal, upper_diagonal


def tridiagonal_func(lower_diagonal, diagonal, upper_diagonal, vector_f):
    vector_f = np.array(vector_f, dtype=np.longdouble)
    n = len(diagonal)
    for i in range(1, n):
        if abs(diagonal[i-1]) < 1e-10:
            raise ValueError("Матрица несовместна")
        tmp = lower_diagonal[i-1] / diagonal[i-1]
        diagonal[i] -= tmp * upper_diagonal[i-1]
        vector_f[i] -= tmp * vector_f[i-1]

    vector_x = np.zeros(n, dtype=np.longdouble)

    if abs(diagonal[n-1]) < 1e-10:
        raise ValueError("Матрица несовместна")

    vector_x[n-1] = vector_f[n-1] / diagonal[n-1]

    for i in range(n-2, -1, -1):
        if abs(diagonal[i]) < 1e-10:
            raise ValueError("Матрица несовместна")
        vector_x[i] = (vector_f[i] - upper_diagonal[i] * vector_x[i+1]) / diagonal[i]

    return vector_x
