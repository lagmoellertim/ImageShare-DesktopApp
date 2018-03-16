from cefpython3 import cefpython as cef
import sys
from threading import Thread

class GUI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = False

    def run(self):
        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        cef.Initialize()
        self.running = True
        while True:
            cef.MessageLoop()
        cef.Shutdown()
    
    @staticmethod
    def new_task(func):
        cef.PostTask(cef.TID_UI, func)

    @staticmethod
    def set_javascript_bindings(browser,binding_name,func):
        bindings = cef.JavascriptBindings(
            bindToFrames=False, bindToPopups=False)
        bindings.SetFunction(binding_name, func)
        browser.SetJavascriptBindings(bindings)

    @staticmethod
    def execute_javascript_func(browser, func_name, *args):
        browser.ExecuteFunction(func_name, *args)

    @staticmethod
    def add_browser(instance=None,callback_func_name="",**kwargs):
        browser = cef.CreateBrowserSync(**kwargs)

        if instance and callback_func_name:
            handler = LifespanHandler(instance,callback_func_name)
            browser.SetClientHandler(handler)

        return browser

class LifespanHandler(object):
    def __init__(self, instance,callback_func_name):
        object.__init__(self)
        self.instance = instance
        self.callback_func_name = callback_func_name
    def OnBeforeClose(self, browser):
        getattr(self.instance, self.callback_func_name)()