import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pylab import plot
import seaborn as sns

# Подключаем и читаем файл с данными metal.csv
values_df = pd.read_csv('metal.csv', delimiter=';')

# получение типов данных столбцов
print(values_df.info())

# Вывод названий столбцов таблицы
print(values_df.columns)

# Вывод данных таблицы
print(values_df.head())

# преобразование данных в массив
# приведение типа DataFrame к типу ndArray и выбор 2-го столбца
values_arr2 = np.array(values_df)[:, 2]
print(values_arr2)

# приведение типа DataFrame к типу ndArray и выбор 2-го и 3-го столбца
values_arr23 = np.array(values_df)[:, 2:4]
print(values_arr23)

# визуализация данных
#matplotlib.style.use('ggplot')
plt.figure()
x = np.linspace(values_arr2[0], values_arr23[values_arr2.size - 1], values_arr2.size)
plot(x, values_arr2, 'g')
plt.show()
