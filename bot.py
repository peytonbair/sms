from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from click._compat import raw_input
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime
import threading
import time


class TechnicalIndicators:
    def __init__(self, stock_name):
        self.api_key= "apikey"
        self.stock_name=stock_name
    #    self.macd_data=self.macd()
    #    self.rsi_data=self.rsi()
    #    self.bbands_data=self.bbands()
    #    self.sma_data=self.sma()
    #    self.close_data=self.close()

        #print(self.bbands_data)
        #print(self.rsi_data)
        #print(self.sma_data)
        #print(self.close_data)
        #self.rsi_data['RSI'].plot()
        #plt.show()
        #self.sma_data['SMA'].plot()
        #self.bbands_data['Real Middle Band'].plot()
        #self.close_data['4. close'].plot()
        #plt.show()




    def question(self):
        stock_name=raw_input("Enter stock name:")
        return stock_name
    def macd(self):
        a = TechIndicators(key=self.api_key, output_format='pandas')
        data, meta_data = a.get_macd(symbol=self.stock_name,interval='daily')
        return data

    def rsi(self):
        b=TechIndicators(key=self.api_key,output_format='pandas')
        data,meta_data = b.get_rsi(symbol=self.stock_name,interval='1min',time_period=20)
        return data
    def bbands (self):
        c=TechIndicators(key=self.api_key,output_format='pandas')
        data,meta_data=c.get_bbands(symbol=self.stock_name,interval='1min')
        return data
    def sma(self): #simple moving average
        d= TechIndicators(key=self.api_key, output_format='pandas')
        data, meta_data = d.get_sma(symbol=self.stock_name,interval='1min',time_period=10)

        return data
    def close(self):
        d=TimeSeries(key=self.api_key,output_format='pandas')
        data,meta_data=d.get_intraday(symbol=self.stock_name,outputsize='full',interval='1min')

        #plt.show()
        #print(data)
        return data


class Strategy():
    def __init__(self):
        #run function every minutes
        #threading.Timer(60, Strategy).start()
        self.money = '300'
        self.company = 'AMD'
        self.time = str(Timer().time)
        self.purchased = False
        #get data from TechnicalIndicators class
        self.close_data = TechnicalIndicators(self.company).close()
        self.rsi_data = TechnicalIndicators(self.company).rsi()
        self.bbands = TechnicalIndicators(self.company).bbands()
        self.sma_data = TechnicalIndicators(self.company).sma()
        #time specific data
        #self.rsi = self.rsi_data['RSI']
        #self.rsi = self.rsi[self.time]
        #self.close = self.close_data[self.time]
        #print(self.rsi)
        #print(self.close)

        self.upperband = self.bbands['Real Upper Band']
        self.middleband = self.bbands['Real Middle Band']
        self.lowerband = self.bbands['Real Lower Band']
        self.bandwidth = self.upperband - self.lowerband
        #print(self.upperband)
        #print(self.lowerband)
        #print(self.middleband)

    #    print(self.bandwidth)
    #    self.current_rsi = self.rsi_data['RSI']
    #    self.current_rsi = self.current_rsi[Timer().time]
        self.indicator = 0
        #self.sma_data['SMA'].plot()
        #print(self.bbands)
        #print(self.sma_data)
        #print(self.upperband['2020-1-03 00:00:00'])
        #print(self.middleband['2020-1-03 00:00:00'])
        #print(self.lowerband['2020-1-03 00:00:00'])
        #print(self.rsi_data)
        self.rsi_data['RSI'].plot()
        plt.show()
        #self.sma_data['SMA'].plot()
        self.close_data['4. close'].plot()
        self.upperband.plot()
        self.middleband.plot()
        self.lowerband.plot()

        #self.check()

    def check(self):
        prob = 0
        prob = self.check_bbands() + self.check_rsi()
        if(self.purchased):
            if(prob <= -1.5):
                self.sell()
        else:
            if(prob >= 1.5):
                self.buy()

    def check_bbands(self):
        prob = 0
        if(self.close <= self.lowerband):
            prob = prob + 1
        elif(self.close >= self.upperband):
            prob = prob - 1

        elif(self.close <= self.middleband):
            prob = prob + .5
        elif(self.close >= self.middleband):
            prob = prob - .5

        return prob

    def check_rsi(self):
        prob = 0
        if(self.rsi >= 70):
            prob = prob - 1
        elif(self.rsi <= 30):
            prob = prob + 1
        elif(self.rsi >= 60):
            prob = prob - .5
        elif(self.rsi <= 40):
            prob = prob + .5
        return prob

    def check_macd(self):
        prob = 0
        return prob



    def buy(self, price):
        self.money = self.money - price
        self.purchased = True
    def sell(self, price):
        self.money = self.money + price
        self.purchased = False



#deal with time and get
class Timer():
    def __init__(self):
        self.minute = (datetime.now().strftime('%M'))
        self.hour =   str(int(datetime.now().strftime('%H'))+2)
        self.day =    (datetime.now().strftime('%d'))
        self.month =  (datetime.now().strftime('%m'))
        self.year =   (datetime.now().strftime('%Y'))
        self.date = self.year + '-'+ self.month + '-' + self.day
        self.time =   str(self.year + '-' + self.month + '-' + self.day + ' ' + self.hour + ':' + self.minute + ':00')




if __name__ == '__main__':

    Strategy()
