import gui
import tasks
import system_tray
import time
from tools.global_queue import GlobalQueue
from PIL import Image, ImageDraw
import server
from tools import ip
import config
import os

class Main:
    def __init__(self,image):
        self.image_queue = GlobalQueue() #Initializing a Gl obalQueue for incoming Images

        self.__stop = False

        self.upload_path = os.path.abspath(config.upload_path)
        self.token = config.token

        self.server = server.Server(__name__, config.port)
        self.main_view = server.MainView()
        self.main_view.set_attr(self.image_queue,self.upload_path,self.token)
        self.server.add_view_method("/",self.main_view.as_view("main"))
        self.server.setDaemon = True

        self.gui = gui.GUI()
        self.gui.setDaemon = True

        self.system_tray = system_tray.SystemTray("ImageShare") #Setting up Tray Icon and Menu
        self.system_tray.system_tray.menu = system_tray.Menu(
            system_tray.MenuItem("Gallery",action=self.start_gallery_task,default=True),
            system_tray.MenuItem("QR-Code",action=self.start_qr_code_task),
            system_tray.MenuItem("Stop",action=self.stop_system_tray_task)            
        )

        self.system_tray.system_tray.icon = image

    def start(self):
        self.server.start() #Starting all threads and the blocking system_tray
        self.gui.start()
        time.sleep(1)
        self.start_qr_code_task() #Show QR-Code after Application Start
        self.system_tray.run()

    def start_gallery_task(self,*args):
        queue = self.image_queue.get_new_queue()
        self.gallery_task = tasks.Gallery(queue, self.upload_path)
        self.gallery_task.setDaemon = True
        self.gui.new_task(self.gallery_task.task)

    def start_qr_code_task(self,*args):
        self.qr_code_task = tasks.QRCode("http://{}:{}/?key={}".format(ip.get_ip(),
            config.port,
            self.token))
        self.qr_code_task.setDaemon = True
        self.gui.new_task(self.qr_code_task.task)

    def stop_system_tray_task(self,*args):
        self.system_tray.system_tray.stop()
        self.__stop = True

image = Image.open("resources/icon.ico")

m = Main(image)
m.start()