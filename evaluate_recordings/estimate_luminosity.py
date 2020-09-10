from glob import glob
from os.path import join

from PIL import Image
import numpy as np

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale


#folder = "2020-08-11-15-31-14-753487"
folder = "backup_data/2020-07-11-03-31-27-071514"
images = glob(join(folder, "*.png"))
if __name__ == '__main__':
    total_brightness = []
    for file in images:
        image = Image.open(file)
        brightness = calculate_brightness(image)
        total_brightness.append(brightness)
        print("%s\t%s" % (file, brightness))
    print(np.mean(total_brightness))
