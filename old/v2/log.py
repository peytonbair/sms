import json
from datetime import datetime

class Log():
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
