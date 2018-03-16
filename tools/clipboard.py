from io import BytesIO
import win32clipboard
from PIL import Image

class Clipboard:
    @classmethod
    def image_to_clipboard(cls,path):
        path = path.replace("file:///","").replace("file://","")
        image = Image.open(path)

        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        cls.__send_to_clipboard(win32clipboard.CF_DIB, data)

    @staticmethod
    def __send_to_clipboard(clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()