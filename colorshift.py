import base64
import numpy
from random import randrange
import cv2


def color_shifter_filter(image):
    decoded_string = base64.decodebytes(image)
    jpg_as_np = numpy.frombuffer(decoded_string, dtype=numpy.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    shift_h = (h + randrange(12) * 19) % 255
    shift_hsv = cv2.merge([shift_h, s, v])
    shift_img = cv2.cvtColor(shift_hsv, cv2.COLOR_HSV2BGR)

    converted = cv2.imencode('.jpg', shift_img)[1].tostring()
    jpg_as_text = base64.b64encode(converted).decode('utf-8')
    data = '{"data": "' + jpg_as_text + '"}'

    return data.encode('utf-8')
