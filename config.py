import configparser
import os


class Config:
    """
    Reads and/or writes the configuration from/to a file
    """

    def __init__(self, path):
        """
        Initializes the parameters and checks if a config file is already existing.
        :param path:
        """

        self.path = path
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        if os.path.isfile(path):
            try:
                self.config.read(path)
            except Exception as e:
                print(e)
                self.new_config()
        else:
            self.new_config()

    def new_config(self):
        """
        Creates a new config file with the standart attributes.
        :return:
        """

        self.config["SERVER"] = {
            "AutoDetectIP": "yes",
            "StaticIP": "no",
            "Port": "80"
        }
        self.config["WINDOW"] = {
            "OneInstance": "yes"
        }
        self.config["UPLOAD"] = {
            "UploadPath": "uploads/",
            "ClearUploadsAfterSession": "yes"
        }
        self.config["TOKEN"] = {
            "StaticToken": "no"
        }
        with open(self.path, 'w') as configfile:
            self.config.write(configfile)
