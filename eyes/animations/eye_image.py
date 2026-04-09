from PIL import Image

def load_and_scale_eye_image(displayWidth, displayHeight):
    width = displayWidth
    height = displayHeight

    image1 = Image.open("Eye.png")
    scaled_width = width
    scaled_height = image1.height * width // image1.width
    image1 = image1.resize((scaled_width, scaled_height), Image.BICUBIC)
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    return image1.crop((x, y, x + width, y + height))
