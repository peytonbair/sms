#Trading bot

from alpha_vantage.techindicators import TechIndicators
#import matplotlib.pyplot as plt
#from click._compat import raw_input
import csv
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime
import threading
import time
import json


#A class to get all the technical indicators for trading, using the alpha_vantage api
class TechnicalIndicators:
    def __init__(self, stock_name):
        self.api_key= "BKI9VUGRMX0R6V47"
        self.stock_name=stock_name
    def question(self):
        stock_name=raw_input("Enter stock name:")
        return stock_name
    def macd(self):
        a = TechIndicators(key=self.api_key, output_format='pandas')
        data, meta_data = a.get_macd(symbol=self.stock_name,interval='daily')
        return data

    def rsi(self):
        b=TechIndicators(key=self.api_key,output_format='pandas')
        data,meta_data = b.get_rsi(symbol=self.stock_name,interval='1min',time_period=14)
        return data
    def bbands (self):
        c=TechIndicators(key=self.api_key,output_format='pandas')
        data,meta_data=c.get_bbands(symbol=self.stock_name,interval='1min')
        return data
    def sma(self): #simple moving average
        d= TechIndicators(key=self.api_key, output_format='pandas')
        data, meta_data = d.get_sma(symbol=self.stock_name,interval='1min',time_period=20)

        return data
    def ema(self): #exponential moving average
        d= TechIndicators(key=self.api_key, output_format='pandas')
        data, meta_data = d.get_ema(symbol=self.stock_name,interval='1min',time_period=10)

        return data
    def close(self):
        d=TimeSeries(key=self.api_key,output_format='pandas')
        data,meta_data=d.get_intraday(symbol=self.stock_name,outputsize='full',interval='1min')
        return data




#main Strategy class, where all the hard data is processed and turned into useable data to make buy and sell decisions
class Strategy():

    def __init__(self):
        #run function every minutes
        threading.Timer(60, Strategy).start()

        self.company = 'ETC-USD'
        self.time = str(Timer().time)
        self.balance = float(self.get_balance())
        self.get_record() # get last action info

        #get data from TechnicalIndicators class
        self.close_data = TechnicalIndicators(self.company).close()
        self.rsi_data = TechnicalIndicators(self.company).rsi()
        self.ema_data = TechnicalIndicators(self.company).ema()
        #self.bbands = TechnicalIndicators(self.company).bbands()
        self.sma_data = TechnicalIndicators(self.company).sma()

        #time specific data
        self.rsi = self.rsi_data['RSI']
        self.rsi_average = self.rsi.mean()
        self.rsi = self.rsi[self.time]

        self.volume = self. close_data['5. volume']
        self.volume_mean = self.volume.mean()
        self.volume = self.volume[self.time]


        self.close = self.close_data['4. close']
        self.close_mean = self.close.mean()
        #self.close5 = self.close.tail(5)
        #self.close5mean = self.close5.mean()
        #print(self.close5mean)
        #self.close.plot()
        #plt.show()
        self.close = self.close[self.time]


        #self.upperband = self.bbands['Real Upper Band']
        #self.middleband = self.bbands['Real Middle Band']
        #self.lowerband = self.bbands['Real Lower Band']
        #self.middleband_average = self.middleband.mean()
    #    self.middleband_slope = (float(self.middleband[self.time-3])-float(self.middleband[self.time])/(3))
    #    self.bandwidth = self.upperband - self.lowerband
    #    self.upperband = self.upperband[self.time]
    #    self.middleband = self.middleband[self.time]
    #    self.lowerband = self.lowerband[self.time]
    #    self.bandwidth = self.bandwidth[self.time]

        self.sma = self.sma_data['SMA']
        self.sma_series = self.sma_data['SMA']
        self.sma = self.sma[self.time]

        self.ema = self.ema_data['EMA']
        self.ema = self.ema[self.time]

        self.rsi_high = self.rsi_data['RSI'].tail(15).max()
        self.rsi_low = self.rsi_data['RSI'].tail(15).min()
        self.volume_high = self.close_data['5. volume'].tail(10).max()

        self.output_data()
        self.check()

    def output_data(self):
        print('Time: ' + str(self.time))
        print('Close: ' + str(self.close))
        print('Volume: ' + str(self.volume))
        print('RSI: ' + str(self.rsi))
        print('EMA: ' + str(self.ema))
        print('SMA: ' + str(self.sma))
        print('Last position: ' + str(self.last_action))
        print('Last position price: ' + str(self.last_price))
        print('')


        #print(self.slope)
    def check(self):
        if(self.last_action == 'sell'):
            self.check_buy()
        else:
            self.check_sell()

    def check_buy(self):
        #previous 12 min minimum rsi_data
        if(self.rsi_low < 30):
	    if(self.volume_high > 3000000):
                if(self.ema > self.sma):
                    self.buy()


    def check_sell(self):
        if(self.rsi_high>65):
            if(self.sma > self.ema):
                self.sell()
	#stop loss
	if(self.close < (self.last_price)*.95):
		self.sell()
    def buy(self):
        self.balance = self.balance - self.close
        purchased = True
        self.record('buy')
        self.update_balance()
        print('purchased for: ' + str(self.close))
        print('Balance: '+ str(self.balance))

    def sell(self):
        self.balance = self.balance + self.close
        purchased = False
        self.record('sell')
        self.update_balance()
        print('Sold for: ' + str(self.close))
        print('Balance: '+ str(self.balance))

    #def get_last_buy(self):

    def update_balance(self):

        file = open("balance.txt", 'w')
        file.write(str(self.balance))


    def get_balance(self):
        file = open("balance.txt", 'r')
        for line in file:
            return line

        file.close()

    def record(self,action):
        with open('record.json', 'a+') as file:
            try:
                self.details = json.load(file)
            except:
                self.details = {}
                self.details['transaction'] = []

            self.details['transaction'].insert(0,{
                'name': self.company,
                'action': action,
                'time': self.time,
                'price': self.close,
                'balance': self.balance
            })
            file.truncate(0)
            file.write(json.dumps(self.details, indent=4, sort_keys=True))




    def get_record(self):
        with open('record.json', 'r') as file:

            try:
                self.data = json.load(file)
                self.last_action = self.data['transaction'][0]['action']
                self.last_price = self.data['transaction'][0]['price']

            except:

                self.last_action = 'sell'
                self.last_price = 0



class log():
    def __init__(self):
        self.time = str(datetime.now())
        self.log_time()

    def log_time(self):
        with open('time_log.json', 'a+') as file:
            try:
                self.details = json.load(file)
            except:
                self.details = {}
                self.details['starts'] = []

            self.details['starts'].insert(0,{
                'time': self.time,
                'action': 'start'

            })
            file.truncate(0)
            file.write(json.dumps(self.details, indent=4, sort_keys=True))
#deal with time and get
class Timer():
    def __init__(self):
        self.minute = self.minute()
        self.hour =   self.hour()
        self.day =    (datetime.now().strftime('%d'))
        self.month =  (datetime.now().strftime('%m'))
        self.year =   (datetime.now().strftime('%Y'))
        self.date = self.year + '-'+ self.month + '-' + self.day
        self.time =   str(self.year + '-' + self.month + '-' + self.day + ' ' + self.hour + ':' + self.minute + ':00')

    def minute(self):
        self.minute = (int(datetime.now().strftime('%M'))-5)
        if(self.minute < 10):
            self.minute = '0' + str(abs(self.minute))
        return str(self.minute)
    def hour(self):
        self.hour = (int(datetime.now().strftime('%H'))+2)
        if(self.hour == 24):
            self.hour = '00'
        if(self.hour == 25):
            self.hour = '01'
        return str(self.hour)


if __name__ == '__main__':
    log()
    Strategy()
