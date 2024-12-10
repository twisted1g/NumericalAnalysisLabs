import sys
import differential_equation as de
from PyQt6 import uic
from PyQt6.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('diff_eq.ui', self)

        self.pushButton_1.clicked.connect(self.euler_method)
        self.pushButton_2.clicked.connect(self.second_runge_kutta_method)
        self.pushButton_3.clicked.connect(self.fourth_runge_kutta_method)
        self.pushButton_4.clicked.connect(self.forward_forth_adams_method)
        self.pushButton_5.clicked.connect(self.not_forward_second_adams_method)

    def euler_method(self):
        self.get_data()

        iteration, function_x, function_y = de.forward_euler_method(self.function_string,
                                                                    self.start_condition, self.upper_limit, 0.001)
        print(function_y[-1])
        self.label.setText(str(iteration))
        self.draw_graphic(function_x, function_y)

    def second_runge_kutta_method(self):
        self.get_data()

        iteration, function_x, function_y = de.second_runge_kutta_method(self.function_string,
                                                                    self.start_condition, self.upper_limit, 0.001)

        print(function_y[-1])

        self.label.setText(str(iteration))
        self.draw_graphic(function_x, function_y)

    def fourth_runge_kutta_method(self):
        self.get_data()

        iteration, function_x, function_y = de.fourth_runge_kutta_method(self.function_string,
                                                                    self.start_condition, self.upper_limit, 0.001)

        print(function_y[-1])

        self.label.setText(str(iteration))
        self.draw_graphic(function_x, function_y)

    def forward_forth_adams_method(self):
        self.get_data()

        iteration, function_x, function_y = de.forward_forth_adams_method(self.function_string,
                                                                         self.start_condition, self.upper_limit, 0.001)

        print(function_y[-1])

        self.label.setText(str(iteration))
        self.draw_graphic(function_x, function_y)

    def not_forward_second_adams_method(self):
        self.get_data()

        iteration, function_x, function_y = de.not_forward_second_adams_method(self.function_string,
                                                                          self.start_condition, self.upper_limit, 0.001)

        print(function_y[-1])

        self.label.setText(str(iteration))
        self.draw_graphic(function_x, function_y)

    def draw_graphic(self, function_x, function_y):
        self.graphicsView.clear()
        self.graphicsView.plot(function_x, function_y, pen='r')

    def get_data(self):
        self.lower_limit = float(self.lineEdit_low.text())
        self.upper_limit = float(self.lineEdit_high.text())
        self.function_string = self.lineEdit_func.text()
        self.start_condition = self.lineEdit_start_condition.text()


if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())

