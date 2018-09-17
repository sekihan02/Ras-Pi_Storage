# -*- coding: utf-8 -*-
 
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2, time
 
# フレームサイズ
FRAME_W = 320
FRAME_H = 192
 
# 正面の顔検出用
# cascPath = '/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml'
cascPath = './haarcascades/haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
 
camera = PiCamera()
camera.resolution = (FRAME_W, FRAME_H)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(FRAME_W, FRAME_H))
time.sleep(0.1)
 
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
 
    frame = image.array
    # frame = cv2.flip(frame, -1) # 上下反転する場合
 
    # Convert to greyscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist( gray )
 
    # 顔検出
    faces = faceCascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))
 
    # 検出した顔に枠を書く
    for (x, y, w, h) in faces:
        # 見つかった顔を矩形で囲む
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
    frame = cv2.resize(frame, (540,300))
 
    # ビデオに表示 
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1) & 0xFF
 
    rawCapture.truncate(0)
 
    if key == ord("q"):
        break
 
cv2.destroyAllWindows()
