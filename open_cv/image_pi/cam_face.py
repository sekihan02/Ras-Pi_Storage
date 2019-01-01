# coding:utf-8
# usbカメラの映像表示
# 物体検出器
import argparse
import cv2
from timeit import default_timer as timer


parser = argparse.ArgumentParser()
parser.add_argument('video')
args = parser.parse_args()

# 正面の顔検出用
# cascPath = '/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml'

# 自作検出器
cascPath = './cascade.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

if args.video == '0':
    # 動画撮影オブジェクト
    cam = cv2.VideoCapture(0)
else:
    cam = cv2.VideoCapture(args.video)
if not cam.isOpened():
    raise ImportError('Not open camera or video file.')
# アスペクト比の計算
w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(w)
print(h)

accum_time = 0
curr_fps = 0
fps = 'FPS -> '
prev_time = timer()

frame_count = 1
while True:
    ret, frame = cam.read()
    if ret == False:
        print('Done!')
        break

    # Resized
    im_size = (300, 300)
    resized = cv2.resize(frame, im_size)

    # =================================
    # Image Preprocessing
    # =================================

    # =================================
    # Main Processing
    # result = resized.copy() # dummy
    result = frame.copy() # no resize
    # =================================

    # Calculate FPS
    curr_time = timer()
    exec_time = curr_time - prev_time
    prev_time = curr_time
    accum_time = accum_time + exec_time
    curr_fps = curr_fps + 1
    if accum_time > 1:
        accum_time = accum_time - 1
        fps = 'FPS -> ' + str(curr_fps)
        curr_fps = 0

    # Draw FPS in top right corner
    cv2.rectangle(result, (250, 0), (300, 17), (0, 0, 0), -1)
    cv2.putText(result, fps, (255, 10),
    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

    # Draw Frame Number
    # 顔検出
    faces = faceCascade.detectMultiScale(result, 1.1, 3, 0, (10, 10))
 
    # 検出した顔に枠を書く
    for (x, y, w, h) in faces:
        # 見つかった顔を矩形で囲む
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Output Result
    cv2.imshow('Result', result)

    # Stop Processing
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1