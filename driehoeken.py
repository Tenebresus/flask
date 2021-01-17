import base64

import numpy
import numpy as np
import cv2
import random as rand

from delaunay2D import Delaunay2D


def getcolor(img, points):
    height = img.shape[0]
    width = img.shape[1]

    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillPoly(mask, points, (255))

    res = cv2.bitwise_and(img, img, mask=mask)

    rect = cv2.boundingRect(points)
    cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
    # cv2.imshow('boi', cropped)
    # cv2.waitKey(0)

    colors, count = np.unique(cropped.reshape(-1, cropped.shape[-1]), axis=0, return_counts=True)
    count[0] = 0
    color = colors[count.argmax()]
    return (int(color[0]), int(color[1]), int(color[2]))

def driehoekFilter(img):
    numSeeds = 700
    decoded_string = base64.decodebytes(img)
    jpg_as_np = numpy.frombuffer(decoded_string, dtype=numpy.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    blank_image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    seeds = []
    for i in range(numSeeds):
        p = (rand.randint(0, img.shape[1]), rand.randint(0, img.shape[0]))
        if not p in seeds:
            seeds.append(p)

    center = np.mean(seeds, axis=0)
    dt = Delaunay2D(center, 50 * 800)

    for s in seeds:
        dt.addPoint(s)

    triangles = dt.exportTriangles()

    for t in triangles:
        points = np.array([[seeds[t[0]], seeds[t[1]], seeds[t[2]]]])
        color = getcolor(img, points)
        blank_image = cv2.fillConvexPoly(blank_image, np.int32(points), color)

    converted = cv2.imencode('.jpg', blank_image)[1].tostring()
    jpg_as_text = base64.b64encode(converted).decode('utf-8')
    data = '{"data": "' + jpg_as_text + '"}'

    return data.encode('utf-8')

