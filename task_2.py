import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime

# сглаживание по 3 точкам
def three_points(points):

# сглаживание по 3 точкам
def sqerr(p1, p2):

# Подключаем и читаем файл с данными metal.csv
values_df = pd.read_csv('metal.csv', delimiter=';')

index = 2

# переводим 2 столбец в нампай массив
values_arr = np.array(values_df)[:, index]

print(values_arr)