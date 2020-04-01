from datetime import datetime
import time


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
        self.minute = (int(datetime.now().strftime('%M')))
        if(self.minute < 16):
            self.minute = '00'
        elif(self.minute > 15 & self.minute < 31):
            self.minute = 15
        elif(self.minute > 30 & self.minute < 46):
            self.minute = 30
        else:
            self.minute = 45
        return str(self.minute)
    def hour(self):
        self.hour = (int(datetime.now().strftime('%H'))+2)
        if(self.hour == 24):
            self.hour = '00'
        if(self.hour == 25):
            self.hour = '01'
        return str(self.hour)
