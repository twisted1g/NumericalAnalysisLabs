import sys
import sympy
import numpy
import math
from sympy.parsing.sympy_parser import parse_expr

from PyQt6 import uic
from PyQt6.QtWidgets import *


global_context = {
    'cos': math.cos,
    'sin': math.sin,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'exp': math.exp,
    'log': math.log,
    'pi': math.pi,
    'e': math.e,
}


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MyUI.ui', self)

        self.pushButton_1.clicked.connect(self.MiddleRectangelsMetod)
        self.pushButton_2.clicked.connect(self.SimpsonMetod)


    def GetData(self):
        self.lowLimit = float(self.lineEdit_low.text())
        self.highLimit = float(self.lineEdit_high.text())
        self.epsilon = float(self.lineEdit_eps.text())
        self.functionString = self.lineEdit_func.text()

    def CalculateFunction(self, x):
        return eval(self.functionString, {"__builtins__": None, 'x': x}, global_context)


        #return parse_expr(self.functionString).subs(sympy.Symbol("x"), x)

    def Integral1(self, n):
        h = (self.highLimit - self.lowLimit) / n
        area = 0.0

        for i in range(n):
            midpoint = self.lowLimit + (i + 0.5) * h
            area += self.CalculateFunction(midpoint) * h

        return area

    def IntegralArray1(self, n):
            h = (self.highLimit - self.lowLimit) / n

            for i in range(n):
                yield self.lowLimit + (i + 0.5) * h

    def MiddleRectangelsMetod(self):
        self.GetData()
        s1 = 0
        n = 100
        s2 = self.Integral1(n)

        while abs(s1 - s2) > self.epsilon:
            n *= 2
            s1 = s2
            s2 = self.Integral1(n)

        self.label.setText(str(s2))

        x = numpy.asarray(list(self.IntegralArray1(n)))
        y = numpy.array([])

        for i in range(len(x)):
            if self.CalculateFunction(x[i]) is None:
                x = numpy.delete(x, i)
                continue
            else:
                y = numpy.append(y, self.CalculateFunction(x[i]))


        self.graphicsView.clear()
        self.graphicsView.plot(x, y, pen='r')

    def Integral2(self, n):
        h = (self.highLimit - self.lowLimit) / n
        summa = 0.0

        x0 = self.lowLimit
        x1 = self.lowLimit + h

        for i in range(n):
            summa += self.CalculateFunction(x0) + 4 * self.CalculateFunction(x0 + h / 2) + self.CalculateFunction(x1)
            x0 += h
            x1 += h

        return (h / 6) * summa

    def IntegralArray2(self):
        pass

    def SimpsonMetod(self):
        self.GetData()
        s1 = 0
        n = 100
        s2 = self.Integral2(n)

        while abs(s1 - s2) > self.epsilon:
            n *= 2
            s1 = s2
            s2 = self.Integral2(n)

        self.label.setText(str(s2))

        x = numpy.asarray(list(self.IntegralArray1(n)))
        y = numpy.array([])

        for i in range(len(x)):
            if self.CalculateFunction(x[i]) is None:
                x = numpy.delete(x, i)
                continue
            else:
                y = numpy.append(y, self.CalculateFunction(x[i]))

        self.graphicsView.clear()
        self.graphicsView.plot(x, y, pen='r')


if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())

