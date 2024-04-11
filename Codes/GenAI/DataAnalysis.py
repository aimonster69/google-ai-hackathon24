import time

class DataAnalysis:

    def __init__(self, job):
        self.job = job

    def Execute(self):
        print("This Jobs is your now")
        time.sleep(1)
        return "Working"
