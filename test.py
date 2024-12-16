import numpy as np
import matplotlib.pyplot as plt


def loss_function(w):
    return (w - 1) ** 2


def gradient(w):
    return 2 * (w - 1)


def gradient_descent(w, learning_coef):
    for iteration in range(1000):
        new_w = w - learning_coef * gradient(w)
        print(f"Итерация {iteration+1}: вес = {w}, потеря = {loss_function(w)}")
        if abs(new_w - w) < 0.00001:
            return w
        w = new_w
    return w


optimal_w = gradient_descent(0, 0.1)
print(f"Оптимальное значение w: {optimal_w}")

w_values = np.linspace(-3, 5, 1000)
loss_values = loss_function(w_values)

plt.plot(w_values, loss_values, label='Функция потерь')
plt.scatter(optimal_w, loss_function(optimal_w), color='red')
plt.title('Градиентный спуск')
plt.xlabel('вес')
plt.ylabel('потеря')
plt.legend()
plt.show()
