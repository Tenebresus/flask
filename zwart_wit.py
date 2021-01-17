import cv2
import numpy
import base64


def zwart_wit_filter(image):
    decoded_string = base64.decodebytes(image)
    jpg_as_np = numpy.frombuffer(decoded_string, dtype=numpy.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    converted = cv2.imencode('.jpg', gray_image)[1].tostring()
    jpg_as_text = base64.b64encode(converted).decode('utf-8')
    data = '{"data": "' + jpg_as_text + '"}'

    return data.encode('utf-8')


