import sys
import fourier_series as fs
import numerical_integration as ni
import math
from PyQt6 import uic
from PyQt6.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)

        self.pushButton.clicked.connect(self.fourier_series)

    def fourier_series(self):
        epsilon = float(self.lineEditEps.text())
        count = int(self.lineEditCount.text())
        function_string = self.lineEditFunc.text()
        dots = int(self.lineEditDots.text())

        x_points, y_points = fs.fourier_series(function_string,dots, count, epsilon)

        function_x = ni.get_function_points_x(dots, -math.pi, math.pi)
        function_y = ni.get_function_points_y(function_string, function_x)

        self.graphicsView.clear()
        self.graphicsView.plot(function_x, function_y, pen='r')
        self.graphicsView.plot(x_points, y_points, pen='b')



if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())

