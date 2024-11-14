import sys
import numerical_integration as ni
from PyQt6 import uic
from PyQt6.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MyUI.ui', self)

        self.pushButton_1.clicked.connect(self.middle_rectangles)
        self.pushButton_2.clicked.connect(self.simpson_method)
        self.pushButton_3.clicked.connect(self.gauss_method)


    def get_data(self):
        self.low_limit = float(self.lineEdit_low.text())
        self.high_limit = float(self.lineEdit_high.text())
        self.epsilon = float(self.lineEdit_eps.text())
        self.function_string = self.lineEdit_func.text()

    def draw_graphic(self):
        function_x = ni.get_function_points_x(1000, self.low_limit, self.high_limit)
        function_y = ni.get_function_points_y(self.function_string, function_x)

        self.graphicsView.clear()
        self.graphicsView.plot(function_x, function_y, pen='r')

    def middle_rectangles(self):
        self.get_data()

        integral = ni.runge_rule(ni.middle_rectangle_method, self.epsilon, 1 / 3, self.function_string,
                                 self.low_limit, self.high_limit)

        self.label.setText(str(integral))
        self.draw_graphic()

    def simpson_method(self):
        self.get_data()

        integral = ni.runge_rule(ni.simpson_method, self.epsilon, 1 / 15, self.function_string,
                                 self.low_limit, self.high_limit)

        self.label.setText(str(integral))
        self.draw_graphic()

    def gauss_method(self):
        self.get_data()

        integral = ni.gauss_method_fourth_power(self.function_string, self.low_limit, self.high_limit)

        self.label.setText(str(integral))
        self.draw_graphic()


if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())

