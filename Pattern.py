import csv

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

ACT_SHORT = 0
ACT_LONG = 1

STOP_LIMIT = -15
EXIT_LIMIT = 35

def avgList(y_list, avg_range):
  length = len(y_list)
  avg_y_list = y_list[0:avg_range]
  for i in range(avg_range,length):
    avg_y_list.append(np.mean(y_list[i-avg_range:i]))
  return avg_y_list

def movingAvgCrossover(x_list, y_list):
  length = len(x_list)
  
  list_1 = avgList(y_list, 50)
  list_2 = avgList(y_list, 20)
  list_3 = avgList(y_list, 5)

  short_list = []
  long_list = []

  for i in range(500,len(x_list)-500):
    if list_1[i] > list_2[i] and list_1[i+1] < list_2[i+1]:
      if list_3[i] < list_3[i+1]:
        long_list.append(i)

    if list_1[i] < list_2[i] and list_1[i+1] > list_2[i+1]:
      if list_3[i] > list_3[i+1]:
        short_list.append(i)

  return (short_list, long_list)

def profitGain(x_list, y_list, act_list, act):
  if act == ACT_LONG:
    return profitGainLong(x_list, y_list, act_list, STOP_LIMIT, EXIT_LIMIT)
  elif act == ACT_SHORT:
    return profitGainShort(x_list, y_list, act_list, STOP_LIMIT, EXIT_LIMIT)
  return (0, [])

def profitGainShort(x_list, y_list, act_list, stop_limit, exit_limit):
  act_result = []

  sum_profit = 0
  for act_x in act_list:
    act_y = y_list[act_x]
    profit = 0
    hold_cnt = 1
    while True:
      if profit < stop_limit or profit > exit_limit:
        break
      cur_x = act_x + hold_cnt
      profit = act_y - y_list[cur_x]
      hold_cnt += 1

    if profit > 0:
      act_result.append((act_x, True))
    else:
      act_result.append((act_x, False))
  
    sum_profit += profit
  return (sum_profit, act_result)
  
def profitGainLong(x_list, y_list, act_list, stop_limit, exit_limit):
  act_result = []
  
  sum_profit = 0
  for act_x in act_list:
    act_y = y_list[act_x]
    profit = 0
    hold_cnt = 1
    while True:
      if profit < stop_limit or profit > exit_limit:
        break
      cur_x = act_x + hold_cnt
      profit = y_list[cur_x] - act_y
      hold_cnt += 1

    if profit > 0:
      act_result.append((act_x, True))
    else:
      act_result.append((act_x, False))
  
    sum_profit += profit
  return (sum_profit, act_result)


