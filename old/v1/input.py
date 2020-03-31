import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy
import pandas as pd
#https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=GOOGL&interval=1min&apikey=BKI9VUGRMX0R6V47&datatype=csv
#columns = defaultdict(list) # each value in each column is appended to a list

#with open('daily_TGT.csv') as f:
#    reader = csv.DictReader(f) # read rows into a dictionary format
#    for row in reader: # read a row as {column1: value1, column2: value2,...}
#        for (k,v) in row.items(): # go over each column name and value
#            columns[k].append(v) # append the value into the appropriate list
headers = ['timestamp','open','high', 'low', 'close', 'volume']
data = pd.read_csv('intraday_1min_NKE.csv',names=headers)
#data = data.iloc[::-1]


#data.reindex(index=data.index[::-1])
close = data['close']
#print(close)
timestamp = data['timestamp']
money = 1000.00
high = close[0]
low = close[0]
sum = 0
buy_count = 0
sell_count = 0
pre_high = 0
pre_low = 0
purchased = 0
pre_buy = 0
slope = 0
pre_rising = 0
rising = False #True = rising, False = falling
pre_close = 1000000 # big number so we don't buy imediatly without knowing the price
SMA = 0
sell_stats = ''

stats = []

for i in range(len(close), 1, -1):
    i=i-1

    #determine rising/ falling
    if(close[i] > pre_close):
        rising = True
    elif(close[i] < pre_close):
        rising = False
    else:
        rising = False

    #determine SMA
    aa = 0
    for j in range(i, 1):

        aa = aa + float(close[j])
    SMA = aa/i
    print(aa)
    #determine previos low/high
    if(rising != pre_rising):
        if(rising):
            pre_low = close[i]
        else:
            pre_high = close[i]

    #Determine when to buy

    if(close[i]>pre_close):
        if(purchased == 0):
            buy_count += 1
            pre_buy = float(close[i])
            money = money- (float(close[i]))
            purchased = 1
            buy_stats = "Buy: %s"%(close[i])
            stats.append(buy_stats)


#sell

    elif(close[i]< pre_close):
        if(close[i] > pre_buy):
            if(purchased > 0):
                money = money+float(close[i])
                sell_count += 1
                purchased = 0
                sell_stats = "sell: %s"%(close[i])
                stats.append(sell_stats)




    #determine highest value
    if(close[i] > high):
        high = close[i]
    #Deremine lowest value
    if(close[i] < low):
        low = close[i]
    #sum of all values
    sum = sum + float(i)

    #sell at the end of data


    pre_close = close[i]
    pre_rising = rising

if(purchased != 0):

        money = money + float(close[len(close)-1])
        sell_count += 1
        sell_stats = "sell: price: %s"%(close[len(close)-1])
        stats.append(sell_stats)

print('----------')
print(money)
print(buy_count)
print(sell_count)

print(high)
print(low)
print(stats)






#data['4. close'].plot()
#plt.title('Intraday TimeSeries Google')
#plt.show()
