import sys
import numerical_equations as ne
from PyQt6 import uic
from PyQt6.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('numerical_eq.ui', self)

        self.pushButton_1.clicked.connect(self.bisection_method)
        self.pushButton_2.clicked.connect(self.secant_method)
        self.pushButton_3.clicked.connect(self.newton_method)
        self.pushButton_4.clicked.connect(self.simple_iteration_method)

    def bisection_method(self):
        lower_limit = float(self.lineEdit_low.text())
        upper_limit = float(self.lineEdit_high.text())
        function_string = self.lineEdit_func.text()

        res = ne.bisection_method(function_string, lower_limit, upper_limit, 0.00001)
        if res is not None:
            answer, iteration = res
            self.label.setText(str(answer))
            print(iteration)
        else:
            self.label.setText(str("None"))

    def secant_method(self):
        function_string = self.lineEdit_func.text()
        start_condition = self.lineEdit_start_condition.text()
        x_0, x_1 = tuple(map(float, start_condition.split()))

        res = ne.secant_method(function_string, x_0, x_1, 0.00001)
        if res is not None:
            answer, iteration = res
            self.label.setText(str(answer))
            print(iteration)
        else:
            self.label.setText(str("None"))

    def newton_method(self):
        start_condition = self.lineEdit_start_condition.text()
        x_0 = float(start_condition)

        res = ne.newton_method(x_0, 0.00001)
        if res is not None:
            answer, iteration = res
            self.label.setText(str(answer))
            print(iteration)
        else:
            self.label.setText(str("None"))

    def simple_iteration_method(self):
        start_condition = self.lineEdit_start_condition.text()
        x_0 = float(start_condition)

        res = ne.simple_iteration_method(x_0, 0.00001, 2)
        if res is not None:
            answer, iteration = res
            self.label.setText(str(answer))
            print(iteration)
        else:
            self.label.setText(str("None"))


if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())

