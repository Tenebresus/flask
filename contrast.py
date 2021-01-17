import base64
import numpy
import cv2


def contrast_filter(image):
    decoded_string = base64.decodebytes(image)
    jpg_as_np = numpy.frombuffer(decoded_string, dtype=numpy.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    shift_h = (h + 90) % 180
    shift_s = (s + 40) % 80
    shift_v = (v + 60) % 120
    shift_hsv = cv2.merge([shift_h, shift_s, shift_v])
    shift_img = cv2.cvtColor(shift_hsv, cv2.COLOR_HSV2BGR)

    converted = cv2.imencode('.jpg', shift_img)[1].tostring()
    jpg_as_text = base64.b64encode(converted).decode('utf-8')
    data = '{"data": "' + jpg_as_text + '"}'

    return data.encode('utf-8')
