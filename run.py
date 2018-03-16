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
        self.image_queue = GlobalQueue()

        self.upload_path = os.path.abspath(config.upload_path)
        self.token = config.token

        self.server = server.Server(__name__, config.port)
        self.main_view = server.MainView()
        self.main_view.set_attr(self.image_queue,self.upload_path,self.token)
        self.server.add_view_method("/",self.main_view.as_view("main"))


        self.gui = gui.GUI()

        self.system_tray = system_tray.SystemTray("ImageShare")
        self.system_tray.system_tray.menu = system_tray.Menu(
            system_tray.MenuItem("Gallery",action=self.start_gallery_task),
            system_tray.MenuItem("QR-Code",action=self.start_qr_code_task)
        )
    
        self.system_tray.system_tray.icon = image

    def start(self):
        self.server.start()
        self.gui.start()
        self.system_tray.run()

    def start_gallery_task(self,*args):
        queue = self.image_queue.get_new_queue()
        self.gallery_task = tasks.Gallery(queue, self.upload_path)
        self.gui.new_task(self.gallery_task.task)

    def start_qr_code_task(self,*args):
        self.qr_code_task = tasks.QRCode("http://{}:{}/?key={}".format(ip.get_ip(),
            config.port,
            self.token))
        self.gui.new_task(self.qr_code_task.task)

width = 50
height = 50
color1 = (0,255,0)
color2 = (255,0,0)

image = Image.new('RGB', (width, height), color1)
dc = ImageDraw.Draw(image)
dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
dc.rectangle((0, height // 2, width // 2, height), fill=color2)

m = Main(image)
m.start()