import base64

from PIL import ImageDraw, Image
import random
import math
import cv2
import numpy as np
from matplotlib import cm


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def cirkelFilter(img, count):
    decoded_string = base64.decodebytes(img)
    jpg_as_np = np.frombuffer(decoded_string, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    width, height, _ = img.shape
    blank_image = np.zeros((width, height, 3), np.uint8)

    circles = []
    number_circles = 0

    while number_circles < count:
        no_overlap = False
        new_circle = Circle(random.randint(0, int(width - 1)), random.randint(0, int(height - 1)),
                            random.randint(5, 30))

        for circle in circles:
            if calculateDistance(new_circle.x, new_circle.y, circle.x, circle.y) > new_circle.r + circle.r:
                no_overlap = True
            else:
                no_overlap = False
                break

        if len(circles) == 0:
            no_overlap = True

        if no_overlap:
            color = int(img[new_circle.x, new_circle.y][0]), int(img[new_circle.x, new_circle.y][1]), int(
                img[new_circle.x, new_circle.y][2])
            blank_image = cv2.circle(blank_image, (new_circle.y, new_circle.x), new_circle.r, color, -1)
            circles.append(new_circle)
            number_circles += 1

    converted = cv2.imencode('.jpg', blank_image)[1].tobytes()
    jpg_as_text = base64.b64encode(converted).decode('utf-8')
    data = '{"data": "' + jpg_as_text + '"}'

    return data.encode('utf-8')
