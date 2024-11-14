import sys
import numpy as np
import matrix_solve as ms

from PyQt6 import uic
from PyQt6.QtWidgets import *

class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('matrixCalc.ui', self)

        self.pushButtonGauss.clicked.connect(self.gauss_method)
        self.pushButtonTridiagonal.clicked.connect(self.tridiagonal_matrix_method)

    def gauss_method(self):
        self.read_matrix()
        self.get_data()
        try:
            ms.gauss_func(self.matrix)
            answer, vector_x = ms.write_gauss_answer(self.matrix)
            self.answerBox.setText(answer)
            if self.answerBox.text() != "Система неоднородна":
                residual_vector = ms.find_vector(vector_x, self.matrix_a, self.matrix_b)
                self.label.setText(np.array2string(residual_vector))
        except ValueError as exp:
            print(exp)

    def tridiagonal_matrix_method(self):
        self.read_matrix()
        self.get_data()
        try:
            lower_diagonal, diagonal, upper_diagonal = ms.get_diagonal(self.matrix_a)
            vector_x = ms.tridiagonal_func(lower_diagonal, diagonal, upper_diagonal, self.matrix_b)

            answer = ""
            for i in range(len(vector_x)):
                answer += f"x_{i} = {vector_x[i]}\n"
            self.answerBox.setText(answer)

            residual_vector = ms.find_vector(vector_x, self.matrix_a, self.matrix_b)
            self.label.setText(np.array2string(residual_vector))
        except ValueError as exp:
            print(exp)

    def get_data(self):
        self.matrix_a = []
        self.matrix_b = []
        n, m = self.matrix.shape
        for i in range(n):
            for j in range(m):
                if j == m-1:
                    self.matrix_b.append(self.matrix[i][j])
                else:
                    self.matrix_a.append(self.matrix[i][j])

        self.matrix_a = np.asarray(self.matrix_a, dtype=np.longdouble).reshape((n, m-1))
        self.matrix_b = np.asarray(self.matrix_b, dtype=np.longdouble)

    def read_matrix(self):
        s = str(self.textBox.toPlainText()).splitlines()
        self.matrix = []
        for n in s:
            a = list(map(int, n.split()))
            self.matrix.append(a)
        self.matrix = np.asarray(self.matrix, dtype=np.longdouble)


if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())