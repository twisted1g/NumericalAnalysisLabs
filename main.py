import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *
import newton_interp as ni


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)

        self.pushButton.clicked.connect(self.newton_interpolation)

    def draw_graph(self, x: list[float], y: list[float], color: str):
        self.graphicsView.plot(x, y, pen=color)

    def newton_interpolation(self):
        count = int(self.lineEditCount.text())
        function_string = self.lineEditFunc.text()
        lower = int(self.lineEditLower.text())
        upper = int(self.lineEditUpper.text())

        x_interpolation = ni.get_function_points_x(count, lower, upper, 1)
        y_interpolation = ni.get_function_points_y(function_string, x_interpolation)

        x_points = ni.get_function_points_x(count, lower, upper, 10)
        y_points = ni.get_function_points_y(function_string, x_points)
        y_newton_interpolation = ni.get_newton_polynomial(x_points, x_interpolation, y_interpolation)

        self.graphicsView.clear()
        self.draw_graph(x_points, y_points, "r")
        self.draw_graph(x_points, y_newton_interpolation, "b")


if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())

