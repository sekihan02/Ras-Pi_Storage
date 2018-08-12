#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img = cv2.imread('image.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

if len(face) > 0:
    for rect in face:
        cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0,255), thickness=2)
else:
    print "no face"

cv2.imwrite('detected.jpg', img)
