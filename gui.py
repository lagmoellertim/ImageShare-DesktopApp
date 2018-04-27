from cefpython3 import cefpython as cef
import sys
from threading import Thread


class GUI(Thread):
    """
    This class handles the management of windows and all GUI tasks in general.
    """

    def __init__(self):
        """
        Initializes all necessary parameters.
        """

        Thread.__init__(self)
        self.running = False
        self.stop = False

    def run(self):
        """
        Initializes CEF and runs in a loop.
        :return:
        """

        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        self.running = True
        while not self.stop:
            cef.MessageLoop()
        cef.Shutdown()

    @staticmethod
    def new_task(func):
        """
        Creates an async task (used to create browsers after starting main GUI loop)
        :param func: Function which contains the blueprint of a window
        :return:
        """

        cef.PostTask(cef.TID_UI, func)

    @staticmethod
    def set_javascript_bindings(browser, binding_name, func):
        """
        Used to make Python functions callable from within JavaScript
        :param browser: The browser/window object
        :param binding_name: Name that is called in javascript which is then linked to the real python function
        :param func: A python function which should be called
        :return:
        """

        bindings = cef.JavascriptBindings(
            bindToFrames=False,
            bindToPopups=False
        )
        bindings.SetFunction(binding_name, func)
        browser.SetJavascriptBindings(bindings)

    @staticmethod
    def execute_javascript_func(browser, func_name, *args):
        """
        Used to call JavaScript function from within Python
        :param browser: The browser/window object
        :param func_name: The name of the javascript function which should be called
        :param args: The arguments that should be passed on to the JavaScript function
        :return:
        """

        browser.ExecuteFunction(func_name, *args)

    @staticmethod
    def add_browser(instance=None, callback_func_name="", **kwargs):
        """
        Used to create new browser window, with optional on_close callback handler
        :param instance: The instance of the callback function
        :param callback_func_name: The function which should be called when the window is closed
        :param kwargs: Other arguments that are passed on to the cef browser creation function
        :return:
        """
        browser = cef.CreateBrowserSync(**kwargs)

        if instance and callback_func_name:
            handler = LifespanHandler(instance, callback_func_name)
            browser.SetClientHandler(handler)

        return browser


class LifespanHandler(object):
    """
    Used to detect if browser window will be closed
    """

    def __init__(self, instance, callback_func_name):
        """
        Initializes the necessary values to later execute a callback
        :param instance: The instance of the callback function
        :param callback_func_name: The function which should be called when the window is closed
        """

        object.__init__(self)
        self.instance = instance
        self.callback_func_name = callback_func_name

    def OnBeforeClose(self, browser):
        """
        Gets called by cef when the browser/window instance is going to be closed.
        :param browser: Argument is supplied by cef, but is not needed
        :return:
        """

        getattr(self.instance, self.callback_func_name)()
