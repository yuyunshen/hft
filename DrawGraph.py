import csv
import time

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

def loadData(file_name):
  result = []
  reader = csv.reader(open(file_name))
  # Skip header line.
  reader.next()
  time_list = []
  price_list = []
  num = 0
  for time_str, buy_one_price, newest_price, sell_one_price, count, avg_price, buy_one_count, sell_one_count in reader:
    time_list.append(num)
    price_list.append(float(avg_price))
    num += 1
  return (time_list, price_list, num)

def drawPart(time_list, price_list, highlight_begin, highlight_end, expand_range=50):
  highlight_time_list = time_list[highlight_begin:highlight_end]
  highlight_price_list = price_list[highlight_begin:highlight_end]
  plt.scatter(highlight_time_list, highlight_price_list, s=20, color="red")
  plt.plot(highlight_time_list, highlight_price_list, '--')
  
  expand_begin = highlight_begin - expand_range
  expand_end = highlight_end + expand_range
  expand_time_list = time_list[expand_begin:expand_end]
  expand_price_list = price_list[expand_begin:expand_end]
  plt.scatter(expand_time_list, expand_price_list, s=2, color="blue")
  plt.plot(expand_time_list, expand_price_list, '--')

  plt.grid(True)
  plt.show()

# SUCCESS!
def drawAll(time_list, price_list):
  #plt.scatter(time_list, price_list, s=5)
  plt.plot(time_list, price_list, '--')
  
  list_1 = avgList(price_list, 50)
  #avg_line = plt.plot(time_list, list_1, '-')
  #plt.setp(avg_line, linewidth=1, color='green')

  list_2 = avgList(price_list, 20)
  #avg_line = plt.plot(time_list, list_2, '-')
  #plt.setp(avg_line, linewidth=1, color='red')

  list_3 = avgList(price_list, 5)

  for i in range(500,len(time_list)-500):
    if list_1[i] > list_2[i] and list_1[i+1] < list_2[i+1]:
      if list_3[i] < list_3[i+1]:
        plt.scatter(time_list[i+1], list_2[i+1], s=100, c="black", marker="o")

    if list_1[i] < list_2[i] and list_1[i+1] > list_2[i+1]:
      if list_3[i] > list_3[i+1]:
        plt.scatter(time_list[i+1], list_2[i+1], s=100, c="red", marker="^")

  plt.grid(True)
  plt.show()

def avgList(price_list, avg_range):
  length = len(price_list)
  new_price_list = price_list[0:avg_range]
  for i in range(avg_range,length):
    new_price_list.append(np.mean(price_list[i-avg_range:i]))
  return new_price_list

def mergePoint(time_list, price_list, merge_range):
  length = len(time_list)
  new_length = length / merge_range
  new_time_list = []
  new_price_list = []
  for i in range(new_length):
    new_time_list.append(i*merge_range)
    new_price_list.append(np.mean(price_list[i*merge_range:(i+1)*merge_range]))

  return (new_time_list, new_price_list)

# Fail
def isUpTriangle(value_list, index, up=10, down=4):
  # Monotonic
  begin_index = index - up - down 
  outlier_cnt = 0
  for i in range(up):
    cur_index = begin_index + i
    gap = value_list[cur_index] - value_list[cur_index+1] 
    if gap >= -1:
      if gap < 2:
        outlier_cnt += 1
      else:
        return False
    if outlier_cnt > up / 5:
      return False

  for i in range(down):    
    cur_index = begin_index + up + i
    #if value_list[cur_index] < value_list[cur_index+1] - 1:
    if value_list[cur_index] < value_list[cur_index+1] + 1:
      return False

  return True

def isUpAngleDown(v_list, init=50):
  x_list = range(init)
  y_list = v_list[:init]
  slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x_list, y_list)

  if slope < 2:
    return (False, 0)

  v_max = max(v_list[:init])
  v_min = min(v_list[:init])
  v_gap = v_max - v_min

  x = init

  d_x = 0
  d_x_list = []
  d_y_list = []
  for i in range(init, len(v_list)):
    pre_v = v_list[i-1]
    v = v_list[i]

    if v < v_max:
      if v < v_max - v_gap / 3:
        return (False, 0)
      else:
        if len(d_y_list) == 0:
          d_x_list.append(d_x)
          d_y_list.append(pre_v)
          d_x += 1
        d_x_list.append(d_x)
        d_y_list.append(v)
        d_x += 1

        d_slope, d_intercept, d_r_value, d_p_value, d_slope_std_error = stats.linregress(d_x_list, d_y_list)
        if d_slope < -1:
          return (False, 0)

        if v <= v_max - v_gap / 4 and v > v_max - v_gap / 3:
          if i > 10:
            print v_max, v_min, slope, y_list
            print 
            return (True, i+init)

      v_min = min(v, v_min)
      v_gap = v_max - v_min
    else:
      d_x = 0
      d_x_list = []
      d_y_list = []

      x_list.append(x)
      y_list.append(v)
      x += 1

      slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x_list, y_list)
      if slope < 2:
        return (False, 0)

      v_max = max(v, v_max)
      v_gap = v_max - v_min

  return (False, 0)

"""
if __name__ == "__main__":
  time_list = range(9) 
  price_list = [1,4,4,8,8,10,8,8,8]
  is_up_down, length = isUpAngleDown(price_list)
  print is_up_down, length
  drawAll(time_list[:length-1], price_list[:length-1])
"""
if __name__ == "__main__":
  #time_list, price_list, num = loadData("C:/Users/Rehtal/Desktop/future_3_product/20150728IF1512data.csv")
  time_list, price_list, num = loadData("C:/Users/Rehtal/Desktop/future_3_product/20150729IF1509data.csv")
  
  drawAll(time_list, price_list)

