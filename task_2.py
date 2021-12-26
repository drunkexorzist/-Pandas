import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.metrics import mean_squared_error
from math import sqrt


# функция сглаживания (фильтрации) по 3-м точкам
def three_point(points):
    points1 = np.zeros(len(points))
    size = len(points)
    # все точки
    for i in range(0, len(points) - 1):
        points1[i] = (points[i - 1] + points[i] + points[i + 1]) / 3
    # первая точка
    points1[0] = (5 * points[0] + 2 * points1[1] - points1[2]) / 6
    # последняя точка
    points1[size - 1] = (5 * points[size - 1] + 2 * points1[size - 2] - points1[size - 1]) / 6
    return points1


# функция сглаживания (фильтрации) по 5 точкам
def five_point(points):
    points1 = np.zeros(len(points))
    size = len(points)
    # все точки
    for i in range(0, len(points) - 2):
        points1[i] = (points[i - 2] + points[i - 1] + points[i] + points[i + 1] + points[i + 2]) / 5
    # Первые 2
    points1[1] = (4 * points[0] + 3 * points[1] + 2 * points1[2] + points1[3]) / 10
    points1[0] = (3 * points[0] + 2 * points1[1] + points1[2] - points[3]) / 5
    # Последние 2
    points1[size - 2] = (4 * points[size - 1] + 3 * points[size - 2] + 2 * points1[size - 3] + points1[size - 4]) / 10
    points1[size - 1] = (3 * points[size - 1] + 2 * points1[size - 2] + points1[size - 3] - points[size - 5]) / 5
    return points1


# функция сглаживания (фильтрации) по 7 точкам
def seven_point(points):
    points1 = np.zeros(len(points))
    size = len(points)

    for i in range(0, len(points) - 3):
        points1[i] = (-2 * points[i - 3] + 3 * points[i - 2] + 6 * points[i - 1] + 7 * points[i] + 6 * points[i + 1]
                      + 3 * points[i + 2] - 2 * points[i - 3]) / 21

    # Первые 3
    points1[2] = (-4 * points[0] + 16 * points[1] + 19 * points[2] + 12 * points1[3] + 2 * points1[4] -
                  points1[5] + points1[6]) / 42
    points1[1] = (8 * points[0] + 19 * points[1] + 16 * points1[2] + 6 * points1[3] - 4 * points1[4] -
                  7 * points1[5] + 4 * points1[6]) / 42

    points1[0] = (39 * points[0] + 8 * points1[1] - 4 * points1[2] - 4 * points1[3] + points1[4] +
                  4 * points1[5] - 2 * points1[6]) / 42
    # Последние 3
    points1[size - 3] = (-4 * points[size - 1] + 16 * points[size - 2] + 19 * points[size - 3] +
                         12 * points1[size - 4] + 2 * points1[size - 5] - 4 * points1[size - 6] + points1[
                             size - 7]) / 42

    points1[size - 2] = (8 * points[size - 1] + 19 * points[size - 2] + 16 * points1[size - 3] +
                         6 * points1[size - 4] - 4 * points1[size - 5] - 5 * points1
                         [size - 6] + 4 * points1[size - 7]) / 42

    points1[size - 1] = (39 * points[size - 1] + 8 * points1[size - 2] - 4 * points1[size - 2] -
                         4 * points1[size - 4] + points1[size - 5] + 4 * points1[size - 6] - 2 * points1[size - 7]) / 42
    return points1


# функция вычисления среднеквадратичной ошибки
def sqerr(p1, p2):
    err1 = p1 - p2
    err1 = err1 ** 2
    err2 = sum(err1)
    return err2 / len(p1)


# функция численного диффериенцирования
def differentiation(points, h):
    points1 = np.zeros(len(points))
    size = len(points)

    for i in range(1, len(points) - 1):
        # основной расчет без первой и последней
        points1[i] = (points[i + 1] - points[i - 1]) / 2 * h

    # первая
    points1[0] = (-3 * points[0] + 4 * points[1] - points[2]) / 2 * h
    # последняя
    points1[size - 1] = (3 * points[size - 1] - 4 * points[size - 2] + points
                                    [size - 3]) / 2 * h

    return points1


# Читаем файл
values_df = pd.read_csv('metal.csv', delimiter=';')

# Берем 2 столбец из фрейма
index = 2
values_arr = np.array(values_df)[:, index]

# сглаживание по 3 точкам
points3 = three_point(values_arr)
# среднеквадратичная ошибка
err3 = sqerr(values_arr, points3)

# сглаживание по 5 точкам
points5 = five_point(values_arr)
# среднеквадратичная ошибка
err5 = sqerr(values_arr, points5)

# сглаживание по 7 точкам
points7 = seven_point(values_arr)
# среднеквадратичная ошибка
err7 = sqerr(values_arr, points7)

# <по оси абсцисс - дата>
values_df.Date = values_df.Date.apply(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M'))

values_df.index = values_df.Date
values_arr = pd.DataFrame(np.array(values_df)[:, index])
values_arr.index = values_df.Date

# рисуеи графики сглаженности по 3, 5, 7 точкам
fig, ax = plt.subplots(1, 3)
plt.figure(figsize=(10, 10), dpi=300)

num = 1
points_list = [points3, points5, points7]
for i in range(len(points_list)):
    num += 2
    ax[i].plot(values_arr, 'y', label='Исходный')
    points_df = pd.DataFrame(points_list[i])
    points_df.index = values_df.Date
    ax[i].plot(points_df, 'r', label='Сглаженый')
    ax[i].grid(color='b', linestyle=':')
    ax[i].legend()
    ax[i].set_title(f"Cглаживание по {num} точкам")

fig.set_figheight(8)
fig.set_figwidth(30)
plt.show()

# рисуеи графики 2 и 3 кратной сглаженнсоти
fig, ax = plt.subplots(1, 3)
plt.figure(figsize=(10, 10), dpi=300)

df = points7
count = 1
for i in range(3):
    ax[i].plot(values_arr, 'r', label='Исходное')
    p_df = pd.DataFrame(df)
    p_df.index = values_df.Date
    ax[i].plot(p_df, 'b', label=f'{count} кратное')
    ax[i].grid(color='b', linestyle=':')
    ax[i].legend()
    ax[i].set_title(f"{count} кратное сглаживание")
    df = three_point(df)
    count += 1

fig.set_figheight(8)
fig.set_figwidth(30)
plt.show()

# численное дифириенцирование

a = pd.Series(list(values_arr[0]))
b = pd.Series(list(df))

plt.figure()
plt.plot(values_arr, 'b', label="Исходные")

points_df_2 = pd.DataFrame(df)
points_df_2.index = values_df.Date
plt.plot(points_df_2, 'r', label="3-x кратное сглаживаение")

points_df_dif = pd.DataFrame(differentiation(df, sqerr(a, b)))
points_df_dif.index = values_df.Date
plt.plot(points_df_dif, 'y', label="Численное дифириенцирование")
plt.grid(color='b', linestyle=':')
plt.legend()
plt.show()

# ARIMA
# возьмем 3-х кратно сглаженный фрейм
test_df = df
test_df = test_df.astype('float32')

x = int(len(test_df) * 0.50)
train, test = test_df[0:x], test_df[x:]

# CKO
predictions = train
mse = mean_squared_error(test, predictions)
rmse = sqrt(mse)
print(f'CКО: {rmse}')

history = [x for x in train]
predictions = list()
for i in range(len(test)):
    # predict
    yhat = rmse
    predictions.append(yhat)
    # наблюдение
    obs = test[i]
    history.append(obs)
print('>Прогноз = %.3f, Ожидаемое значение = %3.f' % (yhat, obs))

