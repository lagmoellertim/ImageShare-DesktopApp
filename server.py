from flask import Flask, request
import json
import base64
from flask.views import MethodView
from threading import Thread
import threading
import os
import uuid
from tools import image_rotate

class Server(Thread):
    app = None

    def __init__(self,name,port):
        Thread.__init__(self)
        self.app = Flask(name)
        self.port = port

    def run(self):
        self.app.run(host="0.0.0.0",port=self.port)

    def add_view_method(self, endpoint, view_func):
        self.app.add_url_rule(endpoint, view_func=view_func)

class MainView(MethodView):
    @classmethod
    def set_attr(cls,image_queue,upload_path,token_obj):
        cls.image_queue = image_queue
        cls.upload_path = upload_path
        cls.token_obj = token_obj
    @classmethod
    def post(cls):
        try:
            data = json.loads(request.data)
            
            image_file_type = data["fileformat"]
            image_data = base64.b64decode(data["content"])
            
            token = request.args["key"]
            
            if token != cls.token_obj:
                return "invalid_session"

            filepath = os.path.join(
                cls.upload_path,
                "{}.{}".format(uuid.uuid4(), image_file_type)
            )

            with open(filepath, "wb") as f:
                f.write(image_data)

            image_rotate.auto_rotate(filepath)

            cls.image_queue.put(filepath)
            
            return "success"
        except Exception as e:
            print(e)
            
            return ""