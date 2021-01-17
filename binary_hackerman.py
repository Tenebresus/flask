import cv2
import base64
import numpy


def binary_filter(image):
    decoded_string = base64.decodebytes(image)
    jpg_as_np = numpy.frombuffer(decoded_string, dtype=numpy.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    empty_image = numpy.zeros((img.shape[0], img.shape[1],3), numpy.uint8)

    converted = cv2.imencode('.jpg', img)[1].tobytes()
    jpg_as_text = base64.b64encode(converted).decode('utf-8')

    binary_data = ' '.join(map(bin, bytearray(jpg_as_text, "utf-8")))
    binary_data = binary_data.replace("0b", "")
    binary_data = binary_data[:10000]

    counter = 0
    binary_list = []
    single_binary = " "

    for i in range(10000):
        if binary_data[i] == " ":
            if counter == 10:
                counter = 0
                binary_list.append(single_binary)
                single_binary = " "
            else:
                counter += 1
        single_binary += single_binary.join(binary_data[i])

    height = 20

    for b in binary_list:
        empty_image = cv2.putText(empty_image, b, (-10, height), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
        height += 20

    converted = cv2.imencode('.jpg', empty_image)[1].tostring()
    jpg_as_text = base64.b64encode(converted).decode('utf-8')
    data = '{"data": "' + jpg_as_text + '"}'

    return data.encode('utf-8')
