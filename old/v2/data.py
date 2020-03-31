from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime


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
        data,meta_data = b.get_rsi(symbol=self.stock_name,interval='15min',time_period=14)
        return data
    def bbands (self):
        c=TechIndicators(key=self.api_key,output_format='pandas')
        data,meta_data=c.get_bbands(symbol=self.stock_name,interval='1min')
        return data
    def sma(self): #simple moving average
        d= TechIndicators(key=self.api_key, output_format='pandas')
        data, meta_data = d.get_sma(symbol=self.stock_name,interval='15min',time_period=40)

        return data
    def ema(self): #exponential moving average
        d= TechIndicators(key=self.api_key, output_format='pandas')
        data, meta_data = d.get_ema(symbol=self.stock_name,interval='15min',time_period=20)

        return data
    def close(self):
        d=TimeSeries(key=self.api_key,output_format='pandas')
        data,meta_data=d.get_intraday(symbol=self.stock_name,outputsize='full',interval='15min')
        return data
