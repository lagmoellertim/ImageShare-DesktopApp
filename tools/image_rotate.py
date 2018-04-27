from PIL import Image
import imdirect


def auto_rotate(filepath):
    """
    Rotates an Image based on the EXIF-Information
    :param filepath: Path of the Image
    :return:
    """

    img = Image.open(filepath)
    img_rotated = imdirect.autorotate(img)
    img_rotated.save(filepath)
