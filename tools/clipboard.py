from io import BytesIO
import win32clipboard
from PIL import Image


class Clipboard:
    """
    Copies an Image into the Clipboard
    """

    @classmethod
    def image_to_clipboard(cls, path):
        """
        The Image is opened and converted into a format that the clipboard can handle with.
        :param path: Path to the Image that should be copied
        :return:
        """

        path = path.replace("file:///", "").replace("file://", "")
        image = Image.open(path)

        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        cls.__send_to_clipboard(win32clipboard.CF_DIB, data)

    @staticmethod
    def __send_to_clipboard(clip_type, data):
        """
        Copies the previously generated data from 'image_to_clipboard' into the clipboard
        :param clip_type: Previously in 'image_to_clipboard' generated data
        :param data: Previously in 'image_to_clipboard' generated data
        :return:
        """
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()
