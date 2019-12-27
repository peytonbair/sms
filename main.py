#alpha vantage api-key: BKI9VUGRMX0R6V47
from alpha_vantage.timeseries import TimeSeries
#import matplotlib.pyplot as plt
import json
import time
from datetime import datetime



class info():
    def __init__(self, symbol):
        ts = TimeSeries(key='BKI9VUGRMX0R6V47')

        data, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='compact')
        print(json.dumps(data, indent = 4, sort_keys=True))
        #print(data)
        #with open('data.json', 'w') as f:
        #    json.dump(data, f)
        self.minute = (int(datetime.now().strftime('%M'))) - 2
        self.minute = str(self.minute)
        self.time = datetime.now().strftime('%Y-%m-%d %H:'+self.minute+':00')
        self.current_data = data[self.time]
        self.high = self.current_data['2. high']
        self.low = self.current_data['3. low']
        self.open = self.current_data['1. open']
        self.close = self.current_data['4. close']

        self.money = 1000
        self.history = []

        self.history.append(self.close)
        self.history_average = sum(self.history) / len(self.history)
        print(self.history_average)
        #buy(self.high)


    def buy():
        self.money = self.money - self.high

    def sell():
        print('sell')



class money():
    def __init__(self):
        self.money = 1000


pretime = datetime.now().strftime('%H:%M')


while 1:

    info('NKE')
    sleep(59)






#data['4. close'].plot()
#plt.title('Intraday TimeSeries Google')
#plt.show()
