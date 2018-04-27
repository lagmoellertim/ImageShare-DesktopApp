import gui
import tasks
import time
from tools.global_queue import GlobalQueue
from PIL import Image
import server
from tools import ip, generate_token, object_class
import config
import os
import pystray

class Main:
    """
    The Main class sets up and starts up all the important threads that handle the web server, the GUI, the system tray,
    the gallery and the qr code generation:
    """

    def __init__(self):
        """
        This Method initializes and configures the different parts like the GUI and the web server based on the supplied
        config file.
        """

        image = Image.open("resources/icon/icon.ico")
        self.config = config.Config("config/config.conf")

        self.image_queue = GlobalQueue()

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

        self.active_gallery_windows = []
        self.active_qr_code_windows = []

        self.server = server.Server(__name__,port = self.port)
        self.main_view = server.MainView()
        self.main_view.set_attr(
            self.image_queue,
            self.upload_path,
            self.token
        )

        self.server.add_view_method("/",self.main_view.as_view("main"))
        self.server.setDaemon = True

        self.gui = gui.GUI()
        self.gui.setDaemon = True

        self.one_instance = self.config.config["WINDOW"].getboolean("OneInstance")

        self.system_tray = pystray.Icon("ImageShare")
        self.system_tray.menu = pystray.Menu(
            pystray.MenuItem("Gallery",action=self.start_gallery_task,default=True),
            pystray.MenuItem("QR-Code",action=self.start_qr_code_task),
            pystray.MenuItem("New Session",action=self.start_new_session_task)
        )

        self.new_session_task = tasks.NewSession(
            self.token,
            self.upload_path,
            self.active_gallery_windows,
            self.active_qr_code_windows,
            self.image_queue)
        self.new_session_task.setDaemon = True

        self.system_tray.icon = image

    def start(self):
        """
        This Method starts all the threads the software requires to run. When it is finished, it also opens the
        qr code window so the user can scan the qr code after starting the software. Finally, the blocking
        system tray loop is started.
        :return:
        """

        self.server.start()
        time.sleep(1)
        self.gui.start()
        self.new_session_task.start()
        time.sleep(1)
        self.start_qr_code_task()
        self.system_tray.run()

    def start_gallery_task(self,*args):
        """
        This method is called when the user clicks on the system tray icon. It is used to start the gallery window.
        If the only one instance is allowed, it is checked how many instances of the gallery window are already opened,
        and a new one is only going to be spawned when no other window exists.
        :param args: This param is supplied by the system tray and is not needed.
        :return:
        """

        if len(self.active_gallery_windows) == 0 or not self.one_instance:
            queue = self.image_queue.get_new_queue()
            self.gallery_task = tasks.Gallery(queue, self.upload_path, self.active_gallery_windows)
            self.active_gallery_windows.append(self.gallery_task)
            self.gallery_task.setDaemon = True
            self.gui.new_task(self.gallery_task.task)

    def start_qr_code_task(self,*args):
        """
        This method is called when the user rightclicks on the system tray icon. It is used to start the qr code window.
        If the only one instance is allowed, it is checked how many instances of the gallery window are already opened,
        and a new one is only going to be spawned when no other window exists. The qr code is generated based on the
        IP address, the port and the token of the current session.
        :param args: This param is supplied by the system tray and is not needed.
        :return:
        """

        if len(self.active_qr_code_windows) == 0 or not self.one_instance:
            self.qr_code_task = tasks.QRCode(
                self.ip,
                self.port,
                self.token,
                self.active_qr_code_windows
            )

            self.active_qr_code_windows.append(self.qr_code_task)
            self.qr_code_task.setDaemon = True
            self.gui.new_task(self.qr_code_task.task)

    def start_new_session_task(self,*args):
        """
        This method is called when the user rightclicks on the system tray icon. It is used to start a new session,
        which means that a new token is generated (the old one expires) and the images can be saved and will be
        deleted from the main upload folder.
        :param args: This param is supplied by the system tray and is not needed.
        :return:
        """
        self.new_session_task.start_new_session()

if __name__ == "__main__":
    main = Main()
    main.start()