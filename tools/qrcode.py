import pyqrcode

class QRCode:
    @staticmethod
    def generate_qr_code(content,path):
        code = pyqrcode.create(content)
        code.png(path,scale=10)