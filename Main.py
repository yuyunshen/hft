import BasicFoo
import Pattern

import os

if __name__ == "__main__":
  #x_list, y_list, num = BasicFoo.loadData("../Data/20150729IF1509data.csv")
  #x_list, y_list, num = BasicFoo.loadData("../Data/20150731IF1603data.csv")
  #x_list, y_list, num = BasicFoo.loadData("../Data/20150728IF1512data.csv")
  #x_list, y_list, num = BasicFoo.loadData("../Data/20150729IF1509data.csv")
  x_list, y_list, num = BasicFoo.loadData("../Data/20150729IF1509data.csv")

  cnt = 0
  data_list = os.listdir("../Data")
  for data in data_list:
    print 
    print cnt
    cnt += 1 
    print data

    full_path = "../Data/" + data
    x_list, y_list, num = BasicFoo.loadData(full_path)

    short_list, long_list = Pattern.movingAvgCrossover(x_list, y_list)

    short_sum_profit, short_act_result = Pattern.profitGain(x_list, y_list, short_list, Pattern.ACT_SHORT)

    long_sum_profit, long_act_result = Pattern.profitGain(x_list, y_list, long_list, Pattern.ACT_LONG)
    print short_sum_profit, long_sum_profit

    if short_sum_profit + long_sum_profit < 0:
      print "FAIL!"
      BasicFoo.drawAll(x_list, y_list, short_act_result, long_act_result)
    else:
      print "SUCCESS!"
