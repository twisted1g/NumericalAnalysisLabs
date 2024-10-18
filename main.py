import sys
import interpolation as ip
from PyQt6 import uic
from PyQt6.QtWidgets import *

class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)

        self.pushButtonLagrangeEquals.clicked.connect(self.lagrange_equals_interpolation)
        self.pushButtonLagrangeChebyshev.clicked.connect(self.lagrange_chebyshev_interpolation)
        self.pushButtonSpline.clicked.connect(self.spline_interpolation)

    def get_data(self):
        self.dots = int(self.lineEdit.text())
        self.start = float(self.lineEditLow.text())
        self.end = float(self.lineEditHigh.text())
        self.func_string = self.lineEditFunc.text()

    def draw_graph(self, x: list[float], y: list[float], color: str):
        self.graphicsView.plot(x, y, pen=color)

    def get_original_function(self):
        self.func_points_x = ip.get_function_points_x(self.dots, self.start, self.end, 10)
        self.func_points_y = ip.get_function_points_y(self.func_string, self.func_points_x)

    def lagrange_equals_interpolation(self):
        self.get_data()
        self.get_original_function()

        interpolation_nodes_x = ip.get_function_points_x(self.dots, self.start, self.end)
        interpolation_nodes_y = ip.get_function_points_y(self.func_string, interpolation_nodes_x)

        interpolations_points_y = ip.get_interpolation_function(interpolation_nodes_x,
                                                                interpolation_nodes_y, self.func_points_x)

        self.graphicsView.clear()
        self.draw_graph(self.func_points_x, self.func_points_y, "r")
        self.draw_graph(self.func_points_x, interpolations_points_y, "b")

    def lagrange_chebyshev_interpolation(self):
        self.get_data()
        self.get_original_function()

        chebyshev_nodes_x = ip.get_chebyshev_nodes(self.start, self.end, self.dots)
        chebyshev_nodes_y = ip.get_function_points_y(self.func_string, chebyshev_nodes_x)

        interpolations_points_y = ip.get_interpolation_function(chebyshev_nodes_x,
                                                                chebyshev_nodes_y, self.func_points_x)

        self.graphicsView.clear()
        self.draw_graph(self.func_points_x, self.func_points_y, "r")
        self.draw_graph(self.func_points_x, interpolations_points_y, "b")

    def spline_interpolation(self):
        self.get_data()
        self.get_original_function()

        h = abs(self.start - self.end) / self.dots

        interpolation_nodes_x = ip.get_function_points_x(self.dots, self.start, self.end)
        interpolation_nodes_y = ip.get_function_points_y(self.func_string, interpolation_nodes_x)

        spline_coefficient_a = interpolation_nodes_y
        spline_coefficient_c = ip.spline_calculate_c_coefficient(h, spline_coefficient_a)
        spline_coefficient_b = ip.spline_calculate_b_coefficient(h, spline_coefficient_c, spline_coefficient_a)
        spline_coefficient_d = ip.spline_calculate_d_coefficient(h, spline_coefficient_c)

        spline_coefficient_a = spline_coefficient_a[1:]
        spline_coefficient_c = spline_coefficient_c[1:]

        spline_points_x, spline_points_y = ip.calculate_spline(interpolation_nodes_x, spline_coefficient_a,
                                                               spline_coefficient_b, spline_coefficient_c,
                                                               spline_coefficient_d, 50)

        self.graphicsView.clear()
        self.draw_graph(self.func_points_x, self.func_points_y, "r")
        self.draw_graph(spline_points_x, spline_points_x, "b")

if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())