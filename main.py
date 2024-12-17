import sys
import gradient_descent_method as gd
import numpy as np
from PyQt6 import uic
from PyQt6.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)

        self.pushButton.clicked.connect(self.gradient_descent)

    def gradient_descent(self):
        weight = float(self.lineEditStart.text())
        learning_rate = float(self.lineEditLearingRate.text())
        epsilon = float(self.lineEditEpsilon.text())

        w = gd.gradient_descent(weight, learning_rate, epsilon)
        x = np.linspace(-3, 5, 1000)
        y = [gd.loss_function(i) for i in x]
        self.graphicsView.clear()
        self.graphicsView.plot(x, y, pen='b')
        # scatter = pg.ScatterPlotItem(x=w, y=gd.loss_function(w), pen=pg.mkPen('r'), size=100)
        # self.graphicsView.plot(scatter)
        print(f"Оптимальный вес: {w}")


if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())

