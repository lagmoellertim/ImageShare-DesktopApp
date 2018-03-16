from threading import Thread
import secrets
import time
class Token(Thread):
    def __init__(self,timetable,token_obj):
        Thread.__init__(self)
        self.timetable = timetable

        self.token_obj = token_obj
        self.rangeIndex = None

    def run(self):
        for i, obj in enumerate(self.timetable):
            if i == len(self.timetable)-1:
                break
            if obj <= time.time() < self.timetable[i+1]:
                print(1)
                if self.rangeIndex == None or self.rangeIndex != i:
                    self.rangeIndex = i
                    self.token_obj = self.generate_token()
    
    @staticmethod
    def generate_token():
        return secrets.token_hex(8)


token = ""
oldT = ""
a = Token([time.strptime("18:30","%H:%M"),time.strptime("19:00","%H:%M"),time.strptime("20:00","%H:%M")],token)
print(a.timetable)
a.start()
while 1:
    if token != oldT:
        print(token)
        oldT = token[:]