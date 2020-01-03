from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from click._compat import raw_input
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
class TechnicalIndicators:
    def __init__(self, stock_name):
        self.api_key= "XXXXXXXXXXX"
        self.stock_name=stock_name
    #    self.macd_data=self.macd()
    #    self.rsi_data=self.rsi()
        self.bbands_data=self.bbands()
    #    self.sma_data=self.sma()
        self.close_data=self.close()

        print(self.bbands_data)

        self.close_data['4. close'].plot()
        plt.show()
    #    print(self.close_data)



    def question(self):
        stock_name=raw_input("Enter stock name:")
        return stock_name
    def macd(self):
        a = TechIndicators(key=self.api_key, output_format='pandas')
        data, meta_data = a.get_macd(symbol=self.stock_name,interval='daily')
        return data

    def rsi(self):
        b=TechIndicators(key=self.api_key,output_format='pandas')
        data,meta_data = b.get_rsi(symbol=self.stock_name,interval='daily',time_period=14)
        return data
    def bbands (self):
        c=TechIndicators(key=self.api_key,output_format='pandas')
        data,meta_data=c.get_bbands(symbol=self.stock_name)
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
        self.company = 'NKE'
        self.close_data = TechnicalIndicators(self.company).close_data
        self.bbands = TechnicalIndicators(self.company).bbands_data



Strategy()
