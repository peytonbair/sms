from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
ts = TimeSeries(key='BKI9VUGRMX0R6V47',output_format='pandas')

data, meta_data = ts.get_intraday(symbol='NKE',interval='1min', outputsize='full')

close = data['4. close']

data['4. close'].plot()
print(close)

plt.show()
