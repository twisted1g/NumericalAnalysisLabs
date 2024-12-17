def loss_function(w):
    return (w - 1) ** 2


def gradient(w):
    return 2 * (w - 1)


def gradient_descent(w, learning_rate, epsilon):
    for iteration in range(1000):
        new_w = w - learning_rate * gradient(w)
        print(f"Итерация {iteration+1}: вес = {w}, потеря = {loss_function(w)}")
        if abs(new_w - w) < epsilon:
            return w
        w = new_w
    return w

