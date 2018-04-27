from threading import Thread
import gui
from tools import clipboard, qrcode, generate_token
import os
import tempfile
import uuid
import time
import shutil

import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import askyesno


class Gallery(Thread):
    """
    The Gallery class starts a new window with the image gallery.
    """

    def __init__(self, image_queue, upload_path, active_gallery_windows):
        """
        The gallery class is going to be initialized.
        :param image_queue: A queue where all incoming pictures are put in
        :param upload_path: The path where the images are going to be stored
        :param active_gallery_windows: A list of all currently active gallery windows
        """

        Thread.__init__(self)
        self.stop = False
        self.image_queue = image_queue
        self.upload_path = upload_path
        self.active_gallery_windows = active_gallery_windows

    def task(self):
        """
        This task is going to be executed in the main UI thread. It handles the browser/window setup for the gallery
        as well as the image to clipboard javascript binding. After that, it starts its own thread and runs in a loop.
        :return:
        """
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
        """
        When this method is called, all previously displayed images from the gallery disappear. This happends for
        example after a new session was started.
        :return:
        """

        gui.GUI.execute_javascript_func(
            self.browser,
            "clear"
        )

    def run(self):
        """
        This method creates a thread which is looping continiously. Everytime a new Image enters the image queue,
        it will be displayed on in the gallery window using a javascript function.
        :return:
        """

        time.sleep(.5)
        while not self.stop:
            if not self.image_queue.empty():
                item = self.image_queue.get()
                gui.GUI.execute_javascript_func(
                    self.browser,
                    "add_image",
                    item
                )

        self.image_queue.delete_queue()

    def on_window_close(self):
        """
        This callback is triggered when the window is going to be closed. It stops the main loop and removes the
        window from the list of currently active windows.
        :return:
        """

        self.stop = True
        self.active_gallery_windows.remove(self)


class QRCode(Thread):
    """
    The QRCode class starts a new window with the qr code.
    """

    def __init__(self, ip, port, token_obj, active_qr_code_windows):
        """
        The QR code class is going to be initialized.
        :param ip: The IP address the server is listing on. It is used to generate the QR code.
        :param port: The post the server is listening on. It is used to generate the QR code.
        :param token_obj: The object which contains the current auth token. It is used to generate the QR code.
        :param active_qr_code_windows: A list of all currently active qr code windows
        """

        Thread.__init__(self)
        self.active_qr_code_windows = active_qr_code_windows
        self.ip = ip
        self.port = port
        self.token_obj = token_obj

    def task(self):
        """
        This task is going to be executed in the main UI thread. It handles the browser/window setup for the qr code
        window. After that, it starts its own thread and runs in a loop.
        :return:
        """

        self.browser = gui.GUI.add_browser(
            url="file:///resources/html/qr_code.html",
            callback_func_name='on_window_close',
            window_title="ImageShare QR Connect"
        )

        self.start()

    def generate_msg(self):
        """
        This method generates the QR code message based on the ip, the port and the current token.
        :return:
        """

        return "http://{}:{}/?key={}".format(
            self.ip,
            self.port,
            self.token_obj.obj)

    def set_qr_code(self):
        """
        This method generates the qr code message, generates the qr code and injects it into the active window via
        a javascript function.
        :return:
        """

        path = os.path.join(tempfile.gettempdir(), "{}.png".format(uuid.uuid4())).replace("\\", "/")
        qrcode.generate_qr_code(self.generate_msg(), path)

        gui.GUI.execute_javascript_func(
            self.browser,
            "set_qr_code",
            path
        )

    def run(self):
        """
        This method starts a thread which will then asynchronously add the qr code to the window.
        :return:
        """

        self.set_qr_code()

    def on_window_close(self):
        """
        This callback gets executed when the qr code window is closed. It removes the window from the list of
        currently active ones.
        :return:
        """

        self.active_qr_code_windows.remove(self)


class NewSession(Thread):
    """
    When a new session should start, this class handles the whole procedure.
    """

    def __init__(self, token_obj, upload_path, active_gallery_windows, active_qr_code_windows, image_queue):
        """
        This method initializes all the pieces that are needed to start a new session.
        :param token_obj: The object which contains the current auth token.
        :param upload_path: The path where the images are going to be stored
        :param active_gallery_windows: A list of all currently active gallery windows
        :param active_qr_code_windows: A list of all currently active qr code windows
        :param image_queue: A queue where all incoming pictures are put in
        """
        Thread.__init__(self)
        self.token_obj = token_obj
        self.upload_path = upload_path
        self.active_gallery_windows = active_gallery_windows
        self.active_qr_code_windows = active_qr_code_windows
        self.image_queue = image_queue
        self.new_session = False

    def start_new_session(self):
        """
        When this method gets called, the mainloop of the thread opens a dialog to start a new session.
        :return:
        """

        self.new_session = True

    def run(self):
        """
        This method start a thread which contains a continous loop. It handles the creating of new sessions, the
        generation of new tokens, saving the images to a new path, cleaning the standart output folder, cleaning
        the gallery and clearing the queues. To avoid the loss of data, multiple confirmations are needed to start
        a new session.
        :return:
        """

        root = tk.Tk()
        root.withdraw()
        while True:
            if self.new_session:
                if askyesno("New Session", "Are you sure you want to start a new session?"):
                    abort = False if os.listdir(self.upload_path) != [] else True
                    path = ""
                    while not abort:
                        path = asksaveasfilename()
                        if not path:
                            abort = askyesno("Cancel", "Are you sure you don't want to save the image files?")
                        else:
                            break

                    for window in self.active_gallery_windows:
                        window.clear_images()
                    self.token_obj.setValue(generate_token.generate_token())
                    for window in self.active_qr_code_windows:
                        window.set_qr_code()
                    self.image_queue.clear()

                    if not abort:
                        shutil.copytree(self.upload_path, path)
                    shutil.rmtree(self.upload_path)
                    os.mkdir(self.upload_path)

                self.new_session = False
