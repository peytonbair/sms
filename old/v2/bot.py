#!/usr/bin/python

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

from log import Log
from timer import Timer
from data import TechnicalIndicators
#main Strategy class, where all the hard data is processed and turned into useable data to make buy and sell decisions
class Strategy():
    def __init__(self):
        #run function every minutes
        threading.Timer(60, Strategy).start()

        self.company = 'BTC-USD'
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
        self.close = self.close[self.time]

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
        if(self.rsi_low <= 30):
    	    if(self.volume_high > 3000000):
                    if(self.ema > self.sma):
                        self.buy()


    def check_sell(self):
        if(self.rsi_high>=65):
            if(self.sma > self.ema):
                self.sell()
	#stop loss
    	if(self.close < (self.last_price)*.95):
    		self.sell()
    def buy(self):
        self.balance = self.balance - self.close
        self.record('buy')
        self.update_balance()
        print('purchased for: ' + str(self.close))
        print('Balance: '+ str(self.balance))

    def sell(self):
        self.balance = self.balance + self.close
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
                self.last_time = self.data['transaction'][0]['time']
                self.last_action = self.data['transaction'][0]['action']
                self.last_price = self.data['transaction'][0]['price']

            except:

                self.last_action = 'sell'
                self.last_price = 0

#deal with time and get



if __name__ == '__main__':
    Log()
    Strategy()
