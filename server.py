from flask import Flask, request
import json
import base64
from flask.views import MethodView
from threading import Thread
import os
import uuid
from tools import image_rotate


class Server(Thread):
    """
    The Server class runs Flask, the webserver, in a threaded environment
    """
    app = None

    def __init__(self, name, port=80):
        """
        This method initializes the Flask object and saves the port the Flask server will later run on.
        :param port: This is the port the server listens on for new requests, e.g. port 80.
        """

        Thread.__init__(self)
        self.app = Flask(name)
        self.port = port

    def run(self):
        """
        This method starts the Flask webserver in a thread. It listens on the host 0.0.0.0 so that it can be reached
        in every possible way, including 127.0.0.1 as well as other local ip addresses (basically a wildcard).
        :return:
        """
        self.app.run(host="0.0.0.0", port=self.port)

    def add_view_method(self, endpoint, view_func):
        """
        This method adds the handler for a certain url rule, e.g. '/index' (endpoint) -> func_handler (view_func).
        :param endpoint: The url rule, e.g. '/index'.
        :param view_func: The function that should be called on an incoming connection.
        :return:
        """
        self.app.add_url_rule(endpoint, view_func=view_func)


class MainView(MethodView):
    """
    This class creates a view for a certain url rule
    """

    @classmethod
    def set_attr(cls, image_queue, upload_path, token_obj):
        """
        This classmethod basically acts as an '__init__' function, which means it sets up all the class variables that
        are needed in order for the main function to work.
        :param image_queue: A queue where all incoming pictures are put in
        :param upload_path: The path where the images are going to be saved
        :param token_obj: The token object which contains the token string. If it is the same as the token that was
        received from the smartphone, the image is accepted
        :return:
        """

        cls.image_queue = image_queue
        cls.upload_path = upload_path
        cls.token_obj = token_obj

    @classmethod
    def post(cls):
        """
        This method handles all incoming connections that are routed to '/'. The image data is received as a base64
        string which is converted back into the original format. If the token from the request matches with the current
        session token, the image is saved at the specified location. In addition, some images need to be rotated based
        on their EXIF-Information, which is also being done. Finally, the imagepath is put into the image queue.
        :return:
        """

        try:
            data = json.loads(request.data)

            image_file_type = data["fileformat"]
            image_data = base64.b64decode(data["content"])

            token = request.args["key"]

            if token != cls.token_obj.obj:
                return "invalid session"

            filepath = os.path.join(
                cls.upload_path,
                "{}.{}".format(uuid.uuid4(), image_file_type)
            )

            with open(filepath, "wb") as f:
                f.write(image_data)

            try:
                image_rotate.auto_rotate(filepath)
            except Exception as e:
                print(e)

            cls.image_queue.put(filepath)
            return "success"

        except Exception as e:
            print(e)
            return ""
