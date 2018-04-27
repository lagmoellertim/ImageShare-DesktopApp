import pyqrcode


def generate_qr_code(content, path):
    """
    Generates a QR code
    :param content: Text that the QR code should represent
    :param path: Path of where to store the QR code
    :return:
    """

    code = pyqrcode.create(content)
    code.png(path, scale=10)
