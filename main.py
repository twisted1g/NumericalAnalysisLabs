import sys
import numpy as np
import iteration_methods as im
from PyQt6 import uic
from PyQt6.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('iteration_methods.ui', self)
        self.pushButtonOverRelaxation.clicked.connect(self.over_relaxation)
        self.pushButtonSeidel.clicked.connect(self.seidel_method)
        self.pushButtonSteepestDescent.clicked.connect(self.steepest_descent_method)

    def over_relaxation(self):
        self.read_matrix()
        self.get_data()

        vector_x, residual_list, iteration = im.over_relaxation_method(self.matrix_a, self.matrix_b, 0.5, self.epsilon)
        print(iteration)
        self.answerBox.setText(str(vector_x))
        self.draw_graphic(residual_list, iteration)

    def seidel_method(self):
        self.read_matrix()
        self.get_data()

        vector_x, residual_list, iteration = im.seidel_method(self.matrix_a, self.matrix_b, self.epsilon)
        print(iteration)
        self.answerBox.setText(str(vector_x))
        self.draw_graphic(residual_list, iteration)

    def steepest_descent_method(self):
        self.read_matrix()
        self.get_data()

        vector_x, residual_list, iteration = im.steepest_descent_method(self.matrix_a, self.matrix_b, self.epsilon)
        print(iteration)
        self.answerBox.setText(str(vector_x))
        self.draw_graphic(residual_list, iteration)

    def get_data(self):
        self.epsilon = float(self.lineEdit.text())
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

    def draw_graphic(self, residual_list, iteration):
        self.graphicsView.clear()
        self.graphicsView.plot([i for i in range(iteration)], residual_list, pen='r')


if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())