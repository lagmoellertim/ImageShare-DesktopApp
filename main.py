import gui
import tasks
import system_tray
import time
from tools.global_queue import GlobalQueue
from PIL import Image, ImageDraw
import server
from tools import ip, generate_token, object_class
import config
import os
from queue import Queue

class Main:
    def __init__(self,image):
        self.config = config.Config("config/config.conf")

        self.image_queue = GlobalQueue() #Initializing a GlobalQueue for incoming Images
        self.__stop = False

        if self.config.config["SERVER"].getboolean("AutoDetectIP"):
            self.ip = ip.get_ip()
        else:
            self.ip = self.config.config["SERVER"]["StaticIP"]
            
        self.port = int(self.config.config["SERVER"]["Port"])

        self.upload_path = os.path.abspath(self.config.config["UPLOAD"]["UploadPath"])

        self.token = object_class.Object(None)
        if self.config.config["TOKEN"]["StaticToken"].lower() in ["no","false","off",0]:
            self.token.setValue(generate_token.generate_token())
        else:
            self.token.setValue(self.config.config["TOKEN"]["StaticToken"])
        #After new session clear view
        self.clear_view = GlobalQueue()
        self.active_gallery_windows = []
        self.active_qr_code_windows = []

        self.server = server.Server(__name__, self.port)
        self.main_view = server.MainView()
        self.main_view.set_attr(self.image_queue,self.upload_path
        ,self.token)
        self.server.add_view_method("/",self.main_view.as_view("main"))
        self.server.setDaemon = True

        self.gui = gui.GUI()
        self.gui.setDaemon = True

        self.system_tray = system_tray.SystemTray("ImageShare") #Setting up Tray Icon and Menu
        self.system_tray.system_tray.menu = system_tray.Menu(
            system_tray.MenuItem("Gallery",action=self.start_gallery_task,default=True),
            system_tray.MenuItem("QR-Code",action=self.start_qr_code_task),
            system_tray.MenuItem("New Session",action=self.start_new_session_task),
            system_tray.MenuItem("Stop",action=self.stop_system_tray_task)            
        )

        self.new_session_task = tasks.NewSession(
            self.token,
            self.upload_path,
            self.clear_view,
            self.active_gallery_windows,
            self.active_qr_code_windows,
            self.image_queue)
        self.new_session_task.setDaemon = True

        self.system_tray.system_tray.icon = image

    def start(self):
        self.server.start() #Starting all threads and the blocking system_tray
        self.gui.start()
        self.new_session_task.start()
        time.sleep(1)
        self.start_qr_code_task() #Show QR-Code after Application Start
        self.system_tray.run()

    def start_gallery_task(self,*args):
        if len(self.active_gallery_windows) == 0 or not self.config.config["WINDOW"].getboolean("OneInstance"):
            queue = self.image_queue.get_new_queue()
            self.gallery_task = tasks.Gallery(queue, self.upload_path, self.clear_view, self.active_gallery_windows)
            self.active_gallery_windows.append(self.gallery_task)
            self.gallery_task.setDaemon = True
            self.gui.new_task(self.gallery_task.task)

    def start_qr_code_task(self,*args):
        if len(self.active_qr_code_windows) == 0 or not self.config.config["WINDOW"].getboolean("OneInstance"):      
            self.qr_code_task = tasks.QRCode(
                self.active_qr_code_windows,
                self.ip,
                self.port,
                self.token)
            self.active_qr_code_windows.append(self.qr_code_task)
            self.qr_code_task.setDaemon = True
            self.gui.new_task(self.qr_code_task.task)

    def start_new_session_task(self,*args):
        self.new_session_task.start_new_session()

    def stop_system_tray_task(self,*args):
        self.system_tray.system_tray.stop()
        self.__stop = True

image = Image.open("resources/icon/icon.ico")

m = Main(image)
m.start()