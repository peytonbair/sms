#alpha vantage api-key: BKI9VUGRMX0R6V47
from alpha_vantage.timeseries import TimeSeries
#import matplotlib.pyplot as plt
import json
import time
from datetime import datetime



class info():
    def __init__(self, symbol):
        ts = TimeSeries(key='BKI9VUGRMX0R6V47')

        data, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')
        print(json.dumps(data, indent = 4, sort_keys=True))
        #print(data)
        #with open('data.json', 'w') as f:
        #    json.dump(data, f)
        self.minute = (datetime.now().strftime('%M'))
        self.hour =   str(int(datetime.now().strftime('%H'))+2)
        self.day =    (datetime.now().strftime('%d'))
        self.month =  (datetime.now().strftime('%m'))
        self.year =   (datetime.now().strftime('%Y'))
        self.date = self.year + '-'+ self.month + '-' + self.day
        self.time =   str(self.year + '-' + self.month + '-' + self.day + ' ' + self.hour + ':' + self.minute + ':00')
        self.current_data = data[(self.time)]


        self.high = self.current_data['2. high']
        self.low = self.current_data['3. low']
        self.open = self.current_data['1. open']
        self.close = float(self.current_data['4. close'])

        self.money = 1000
        self.history = []

        self.history.append(self.close)
        self.history_average = sum(self.history) / len(self.history)

        hour = 9
        minute = 29
        range = ((self.hour-9)*60) + (self.minute)
        #create data from entire day
        for x in range(range): #390 is the number of minutes in the trading cycle

            minute += 1

            #print(time_specific_data)

            if(minute == 60):
                minute = 00
                hour += 1
            used_minute = str(minute)
            if(minute < 10):
                used_minute = '0' + str(minute)

            time_specific_data = data[self.date + ' ' + str(hour) + ':' + (used_minute) + ':00']
            close = time_specific_data['4. close']


            self.history.append(close)

        print('Time: ')
        print(self.time)
        print('Close: ')
        print(self.close)
        print('Close: ')
        print(self.history)




        #buy(self.high)

    def buy(self):
        self.money = self.money - self.close

    def sell():
        print('sell')



if __name__ == '__main__':
    info('NKE')






#data['4. close'].plot()
#plt.title('Intraday TimeSeries Google')
#plt.show()
