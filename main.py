import sys
import numpy as np

from PyQt6 import uic
from PyQt6.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('matrixCalc.ui', self)

        self.pushButtonGauss.clicked.connect(self.GaussMethod)
        self.pushButtonTridiagonal.clicked.connect(self.TridiagonalMatrixMethod)

    def MakeIdentity(self):
        for currentRowIndex in range(len(self.matrix) - 1, 0, -1):
            currentRow = self.matrix[currentRowIndex]
            for aboveRow in self.matrix[:currentRowIndex]:
                multiplier = aboveRow[currentRowIndex]
                aboveRow -= multiplier * currentRow

    def GaussFunc(self):
        for rowIndex in range(len(self.matrix)):
            pivotIndex = rowIndex + np.argmax(abs(self.matrix[rowIndex:, rowIndex]))
            if pivotIndex != rowIndex:
                self.matrix[[rowIndex, pivotIndex]] = self.matrix[[pivotIndex, rowIndex]]

            currentRow = self.matrix[rowIndex]
            pivotValue = currentRow[rowIndex]

            if abs(pivotValue) < 1e-10:
                raise ValueError("Матрица несовместна")

            currentRow /= pivotValue

            for lowerRow in self.matrix[rowIndex + 1:]:
                factor = lowerRow[rowIndex]
                lowerRow -= factor * currentRow

        self.MakeIdentity()

    def WriteGaussAnswer(self):
        n, m = self.matrix.shape
        self.X = []
        self.answer = ""
        for i in range(n):
            if any(self.matrix[i][j] != 0 for j in range(m - 1) if j != i):
                return "Система неоднородна"
            self.answer += f"x_{i} = {self.matrix[i][m - 1]}\n"
            self.X.append(self.matrix[i][m - 1])

        self.X = np.asarray(self.X, dtype=np.longdouble)
        print(self.matrix)

        return self.answer

    def GaussMethod(self):
        self.ReadMatrix()
        self.GetData()
        try:
            self.GaussFunc()
            self.answerBox.setText(self.WriteGaussAnswer())
            if self.answerBox.text() != "Система неоднородна":
                self.FindVector()
        except ValueError as exp:
            print(exp)

    def GetData(self):
        self.A = []
        self.B = []
        n, m = self.matrix.shape
        for i in range(n):
            for j in range(m):
                if j == m-1:
                    self.B.append(self.matrix[i][j])
                else:
                    self.A.append(self.matrix[i][j])

        self.A = np.asarray(self.A, dtype=np.longdouble).reshape((n, m-1))
        self.B = np.asarray(self.B, dtype=np.longdouble)

    def FindVector(self):
        self.R = []
        n, m = self.A.shape
        for i in range(n):
            self.R.append(0)

        for i in range(n):
            for j in range(m):
                self.R[i] += self.A[i][j] * self.X[j]
            self.R[i] -= self.B[i]
        self.R = np.asarray(self.R, dtype=np.longdouble)
        print(self.R)

        self.label.setText(np.array2string(self.R))

    def TridiagonalFunc(self):
        n, m = self.A.shape
        if (n != m):
            raise ValueError("Матрица не тридиагональная")

        upperDiagonal = []
        diagonal = []
        lowerDiagonal = []

        for i in range(n):
            for j in range(m):
                if i == j:
                    diagonal.append(self.A[i][j])
                elif i == j-1:
                    upperDiagonal.append(self.A[i][j])
                elif i == j+1:
                    lowerDiagonal.append(self.A[i][j])
        lowerDiagonal = np.asarray(lowerDiagonal, dtype=np.longdouble)
        diagonal = np.asarray(diagonal, dtype=np.longdouble)
        upperDiagonal = np.asarray(upperDiagonal, dtype=np.longdouble)


        F = np.array(self.B, dtype=np.longdouble)

        print(F)
        for i in range(1, n):
            if abs(diagonal[i-1]) < 1e-10:
                raise ValueError("Матрица несовместна")
            tmp = lowerDiagonal[i-1] / diagonal[i-1]
            diagonal[i] -= tmp * upperDiagonal[i-1]
            F[i] -= tmp * F[i-1]
        print(F)

        self.X = np.zeros(n, dtype=np.longdouble)


        if abs(diagonal[n-1]) < 1e-10:
            raise ValueError("Матрица несовместна")

        self.X[n-1] = F[n-1] / diagonal[n-1]

        for i in range(n-2, -1, -1):
            if abs(diagonal[i]) < 1e-10:
                raise ValueError("Матрица несовместна")
            self.X[i] = (F[i] - upperDiagonal[i]*self.X[i+1])/diagonal[i]

    def TridiagonalMatrixMethod(self):
        self.ReadMatrix()
        self.GetData()
        try:
            self.TridiagonalFunc()
            self.answer = ""
            for i in range(len(self.X)):
                self.answer += f"x_{i} = {self.X[i]}\n"
            self.answerBox.setText(self.answer)
            self.FindVector()
        except ValueError as exp:
            print(exp)


    def ReadMatrix(self):
        s = str(self.textBox.toPlainText()).splitlines()
        self.matrix = []
        for n in s:
            a = list(map(int, n.split()))
            self.matrix.append(a)
        self.matrix = np.asarray(self.matrix, dtype=np.longdouble)
        print(self.matrix)



if __name__ == "__main__":
    app = QApplication([])
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec())