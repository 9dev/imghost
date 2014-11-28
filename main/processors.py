from PIL import Image

class Watermark(object):
    def process(self, image):
        logo = Image.open(r"resources/imghost.png")
        x = image.size[0] - logo.size[0] - 5
        y = image.size[1] - logo.size[1] - 5
        image.paste(logo, (x,y), logo)
        return image