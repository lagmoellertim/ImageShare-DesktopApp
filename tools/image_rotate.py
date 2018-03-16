from PIL import Image
import imdirect

def auto_rotate(filepath):
    img = Image.open(filepath)
    img_rotated = imdirect.autorotate(img)
    img_rotated.save(filepath)