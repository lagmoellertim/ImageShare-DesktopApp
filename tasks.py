from threading import Thread
import gui
from tools import clipboard, qrcode, generate_token
import os
from cefpython3 import cefpython_py36 as cef
import tempfile
import uuid
import time
import shutil

import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import askyesno

class Gallery(Thread):
    def __init__(self,imageQueue, upload_folder, clear_view, active_windows):
        Thread.__init__(self)
        self.stop = False
        self.imageQueue = imageQueue
        self.upload_folder = upload_folder
        self.clear_view = clear_view
        self.active_windows = active_windows

    def task(self):
        self.browser = gui.GUI.add_browser(
            instance=self,
            callback_func_name='on_window_close',
            url="file:///resources/html/gallery.html",
            window_title="ImageShare Gallery"
        )

        gui.GUI.set_javascript_bindings(
            self.browser,
            "image_to_clipboard",
            clipboard.Clipboard.image_to_clipboard
        )

        self.start()
    def clear_images(self):
        gui.GUI.execute_javascript_func(
                        self.browser,
                        "clear"
                    )

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
        self.active_windows.remove(self)

class QRCode(Thread):
    def __init__(self,active_windows, ip, port, token):
        Thread.__init__(self)
        self.active_windows = active_windows
        self.ip = ip
        self.port = port
        self.token = token
    
    def task(self):
        self.browser = gui.GUI.add_browser(
            url="file:///resources/html/qr_code.html",
            callback_func_name='on_window_close',
            window_title="ImageShare QR Connect"
        )

        self.start()

    def generate_msg(self):
        return "http://{}:{}/?key={}".format(
            self.ip,
            self.port,
            self.token.obj)

    def set_qr_code(self):
        path = os.path.join(tempfile.gettempdir(),"{}.png".format(uuid.uuid4())).replace("\\","/")
        qrcode.QRCode.generate_qr_code(self.generate_msg(),path)

        gui.GUI.execute_javascript_func(
            self.browser,
            "set_qr_code",
            path
        )

    def run(self):
        self.set_qr_code()
    
    def on_window_close(self):
        self.active_windows.remove(self)

class NewSession(Thread):
    def __init__(self, token, upload_path, clear_view, active_gallery_windows, active_qr_code_windows, image_queue):
        Thread.__init__(self)
        self.token = token
        self.upload_path = upload_path
        self.clear_view = clear_view
        self.active_gallery_windows = active_gallery_windows
        self.active_qr_code_windows = active_qr_code_windows
        self.image_queue = image_queue
        self.new_session = False

    def start_new_session(self):
        self.new_session = True
    def run(self):
        root = tk.Tk()
        root.withdraw()
        while True:
            if self.new_session:
                if askyesno("New Session","Are you sure you want to start a new session?"):
                    abort = False if os.listdir(self.upload_path) != [] else True
                    while not abort:
                        path = asksaveasfilename()
                        if not path:
                            abort = askyesno("Cancel","Are you sure you don't want to save the image files?")
                        else: 
                            break
                    
                    self.clear_view.put(True)
                    for window in self.active_gallery_windows:
                        window.clear_images()
                    self.token.setValue(generate_token.generate_token())
                    for window in self.active_qr_code_windows:
                        window.set_qr_code()
                    self.image_queue.clear()
                    
                    if not abort:
                        shutil.copytree(self.upload_path, path)
                    shutil.rmtree(self.upload_path)
                    os.mkdir(self.upload_path)
                    
                self.new_session = False