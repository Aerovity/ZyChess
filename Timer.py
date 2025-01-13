import time
# Clock
class smallClock:
    # Constructor
    def __init__(self, currenttime):
        self.currenttime = currenttime
    def continueTimer(self, Signal):
        if Signal == True:
            time.sleep(1)
            self.currenttime -= 1
    def getTime(self):
        FullTime = []
        minutes = str(self.currenttime // 60)
        seconds = str(self.currenttime % 60)
        if len(minutes) == 1:
            minutes = "0" + minutes
        if len(seconds) == 1:
            seconds = "0" + seconds
        FullTime.append(minutes[0])
        FullTime.append(minutes[1])
        FullTime.append(seconds[0])
        FullTime.append(seconds[1])
        return FullTime
    
Timeeer = smallClock(60)
while False:
    Timeeer.continueTimer(True)
    print (Timeeer.getTime())
