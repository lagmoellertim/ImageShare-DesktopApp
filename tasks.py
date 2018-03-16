from threading import Thread
import gui
from tools import clipboard, qrcode
import os
from cefpython3 import cefpython_py36 as cef
import tempfile
import uuid
import time

class Gallery(Thread):
    def __init__(self,imageQueue, upload_folder):
        Thread.__init__(self)
        self.stop = False
        self.imageQueue = imageQueue
        self.upload_folder = upload_folder

    def task(self):
        self.browser = gui.GUI.add_browser(
            instance=self,
            callback_func_name='on_window_close',
            url="file:///html/gallery.html",
            window_title="ImageShare Gallery"
        )

        gui.GUI.set_javascript_bindings(
            self.browser,
            "image_to_clipboard",
            clipboard.Clipboard.image_to_clipboard
        )

        self.start()

    def run(self):
        time.sleep(.5)
        while not self.stop:
            if not self.imageQueue.empty():
                item = self.imageQueue.get()
                gui.GUI.execute_javascript_func(
                    self.browser,
                    "add_image",
                    item
                )

        self.imageQueue.delete_queue() 

    def on_window_close(self):
        self.stop = True

class QRCode(Thread):
    def __init__(self,qr_code_msg):
        Thread.__init__(self)
        self.qr_code_msg = qr_code_msg
    
    def task(self):
        self.browser = gui.GUI.add_browser(
            url="file:///html/qr_code.html",
            window_title="ImageShare QR Connect"
        )

        self.start()

    def run(self):
        path = os.path.join(tempfile.gettempdir(),"{}.png".format(uuid.uuid4())).replace("\\","/")
        
        qrcode.QRCode.generate_qr_code(self.qr_code_msg,path)

        gui.GUI.execute_javascript_func(
            self.browser,
            "set_qr_code",
            path
        )