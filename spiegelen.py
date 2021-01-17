import cv2
import base64
import numpy
import json


def mirror_filter(image):
    decoded_string = base64.decodebytes(image)
    jpg_as_np = numpy.frombuffer(decoded_string, dtype=numpy.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    flip_horizontal = cv2.flip(img, 1)
    converted = cv2.imencode('.jpg', flip_horizontal)[1].tostring()
    jpg_as_text = base64.b64encode(converted).decode('utf-8')
    data = '{"data": "' + jpg_as_text +'"}'

    return data.encode('utf-8')
