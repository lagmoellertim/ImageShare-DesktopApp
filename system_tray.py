from pystray import *

class SystemTray():
    def __init__(self,name):
        self.system_tray = Icon(name)

    def run(self):
        self.system_tray.run()