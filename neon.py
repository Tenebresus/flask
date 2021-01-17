import base64
import threading
from random import randrange
import math
import cv2
import numpy


def neighbors(radius, rowNumber, columnNumber, img):
    a = img
    return is_valid([[i, j] if i >= 0 and i < len(a) and j >= 0 and j < len(a[0]) else 0
             for j in range(columnNumber - 1 - radius, columnNumber + radius)
            for i in range(rowNumber - 1 - radius, rowNumber + radius)], rowNumber, columnNumber)


def is_valid(elements, x, y):
    return [element for element in elements if element != [x, y]]


def id_to_RGB(n):
    n = ((n ^ n >> 15) * 2246822519) & 0xffffffff
    n = ((n ^ n >> 13) * 3266489917) & 0xffffffff
    n = (n ^ n >> 16) >> 8
    return tuple(n.to_bytes(3, 'big'))


def neon_from_indexes(start, end):
    edgeslist = []
    row = start
    while row > end:
        for col in range(len(img[row])):
            pixelImg = img[row][col]
            pixelEdges = edges[row][col]
            if pixelEdges == 255:
                newcolor = []
                closelist = neighbors(6, row, col, img)
                hasclose = False
                edgeof = False
                if start - row < 2 or row - end < 2:
                    edgeof = True
                else:
                    edgeof = False
                for px in closelist:
                    if px in globaledgeslist and not hasclose:
                        hasclose = True

                        pix = img[px[0]][px[1]]
                        b, g, r = pix[0], pix[1], pix[2]
                        if b >= 100:
                            b -= 50
                        if g >= 100:
                            g -= 30
                        if r >= 100:
                            r -= 10
                        newcolor = [b, g, r]
                    if px in edgeslist and not hasclose:
                        hasclose = True

                        pix = img[px[0]][px[1]]
                        b, g, r = pix[0], pix[1], pix[2]
                        if b >= 100:
                            b -= 50
                        if g >= 100:
                            g -= 30
                        if r >= 100:
                            r -= 10
                        newcolor = [b, g, r]
                    if hasclose:
                        break
                if not hasclose:
                    newcolor = [randrange(5) * 50, randrange(5) * 50, randrange(5) * 50]

                if edgeof:
                    globaledgeslist.append([row, col])
                else:
                    edgeslist.append([row, col])

                img[row][col] = newcolor

            else:
                r = pixelImg[2] / 20
                g = pixelImg[1] / 14
                b = pixelImg[0] / 8
                img[row][col] = [b, g, r]
        row -= 1


def neon_filter(image):
    decoded_string = base64.decodebytes(image)
    jpg_as_np = numpy.frombuffer(decoded_string, dtype=numpy.uint8)

    global img
    global edges
    global globaledgeslist

    img = cv2.imdecode(jpg_as_np, flags=1)

    edges = cv2.Canny(img, 100, 200)

    height = len(img)
    width = len(img[0])

    processes = []
    amountP = math.floor(height / 30)
    globaledgeslist = []

    s = height
    last = height - 1

    for i in range(amountP):
        s -= height / amountP
        a = math.floor(s)

        p = threading.Thread(target=neon_from_indexes, args=(last, a))
        p.start()
        processes.append(p)
        last = a

    for p in processes:
        p.join()

    converted = cv2.imencode('.jpg', img)[1].tostring()
    jpg_as_text = base64.b64encode(converted).decode('utf-8')
    data = '{"data": "' + jpg_as_text + '"}'

    return data.encode('utf-8')