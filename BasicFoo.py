import csv

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

def loadData(file_name):
  result = []
  reader = csv.reader(open(file_name))
  # Skip header line.
  reader.next()
  x_list = []
  y_list = []
  num = 0
  for x_str, buy_one_y, newest_y, sell_one_y, count, avg_y, buy_one_count, sell_one_count in reader:
    x_list.append(num)
    y_list.append(float(avg_y))
    num += 1
  return (x_list, y_list, num)

def drawPart(x_list, y_list, highlight_begin, highlight_end, expand_range=50):
  highlight_x_list = x_list[highlight_begin:highlight_end]
  highlight_y_list = y_list[highlight_begin:highlight_end]
  plt.scatter(highlight_x_list, highlight_y_list, s=20, color="red")
  plt.plot(highlight_x_list, highlight_y_list, '--')
  
  expand_begin = highlight_begin - expand_range
  expand_end = highlight_end + expand_range
  expand_x_list = x_list[expand_begin:expand_end]
  expand_y_list = y_list[expand_begin:expand_end]
  plt.scatter(expand_x_list, expand_y_list, s=2, color="blue")
  plt.plot(expand_x_list, expand_y_list, '--')

  plt.grid(True)
  plt.show()

def drawAll(x_list, y_list, short_list, long_list):
  plt.scatter(x_list, y_list, s=5)
  plt.plot(x_list, y_list, '--')
  
  # Mark short point and long point.
  short_success_list = [x for (x, result) in short_list if result == True]
  short_fail_list = [x for (x, result) in short_list if result == False]
  plt.scatter(short_success_list, [y_list[i] for i in short_success_list], s=100, c="red", marker="o")
  plt.scatter(short_fail_list, [y_list[i] for i in short_fail_list], s=100, c="black", marker="o")

  long_success_list = [x for x, result in long_list if result == True]
  long_fail_list = [x for x, result in long_list if result == False]
  plt.scatter(long_success_list, [y_list[i] for i in long_success_list], s=100, c="red", marker="^")
  plt.scatter(long_fail_list, [y_list[i] for i in long_fail_list], s=100, c="black", marker="^")

  plt.grid(True)
  plt.show()
