from PIL import Image

def scale_image(image1, width, height):
    scaled_height = image1.height * width // image1.width

    image1 = image1.resize((width, scaled_height), Image.BICUBIC)
    x = image1.width // 2 - width // 2
    y = image1.height // 2 - height // 2
    return image1.crop((x, y, x + width, y + height))


def load_and_scale_eye_image(displayWidth, displayHeight):
    image1 = Image.open("eyes/Eye.png")
    return scale_image(image1, displayWidth, displayHeight)

