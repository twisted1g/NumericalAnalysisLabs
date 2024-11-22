import sys
import numpy as np
import eigenvalues_iteration_methods as ei
from PyQt6 import uic
from PyQt6.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('eigenvalues_iteration.ui', self)
        self.pushButtonPowerIterationMethod.clicked.connect(self.power_iteration)
        self.pushButtonRotationMethod.clicked.connect(self.rotation_method)

    def power_iteration(self):
        self.read_matrix()
        self.get_data()

        eigenvalue, iteration = ei.power_iteration_method(self.matrix, self.epsilon)

        self.textBrowserAnswer.setText(str(eigenvalue))
        self.textBrowserIteration.setText(str(iteration))

    def rotation_method(self):
        self.read_matrix()
        self.get_data()

        eigenvalue, iteration = ei.rotation_method(self.matrix, self.epsilon)

        self.textBrowserAnswer.setText(str(eigenvalue))
        self.textBrowserIteration.setText(str(iteration))

    def get_data(self):
        self.epsilon = float(self.lineEdit.text())

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