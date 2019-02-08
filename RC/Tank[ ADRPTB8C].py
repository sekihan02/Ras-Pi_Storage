# coding:utf-8
#!/usr/bin/python
# usbカメラの映像表示
# ADRPTB8Cでラジコン戦車操作
# python Tank.py -l ./model/labels.txt -m ./model/mnist_deep_model.json -w ./model/weights.99.hdf5

# Rasberry-pi
from Adafruit_MotorHAT import Adafruit_MotorHAT
import atexit
import Adafruit_PCA9685
# keras-image
import argparse
from keras.preprocessing.image import array_to_img, img_to_array, load_img
from keras.models import model_from_json
import numpy as np

import cv2
import time
from time import sleep
from timeit import default_timer as timer

# 音声
import subprocess
def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t)
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)

def say(num):
    if num == 0:
        text = '写真とったよー'
    else:
        text = 'や、やめろー'
    jtalk(text)

# 超音波距離センサ reading(0)で距離取得
import RPi.GPIO as GPIO
def reading(sensor):
    TRIG_PIN = 5
    ECHO_PIN = 6

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    if sensor == 0:
        GPIO.setup(TRIG_PIN ,GPIO.OUT)
        GPIO.setup(ECHO_PIN,GPIO.IN)
        GPIO.output(TRIG_PIN , GPIO.LOW)

        sleep(0.3)

        # データ取得開始(取得必要時間10μ秒)
        GPIO.output(TRIG_PIN , True)

        # データ取得のため待機
        sleep(0.00001)
        # データ取得したらパルスを止める
        GPIO.output(TRIG_PIN , False)

        # 距離の取得
        # 超音波を出して前の物体に当たって戻ってkるまでの時間を測定する
        # 開始タイミングの取得
        while GPIO.input(ECHO_PIN) == 0:
          signaloff = time.time()
        # 終了タイミングの取得
        while GPIO.input(ECHO_PIN) == 1:
          signalon = time.time()
        # 物体の距離を計算
        timepassed = signalon - signaloff
        # cmに変換
        distance = timepassed * 17000

        # 距離をcmにして返す
        return distance

    else:
        print ("Incorrect usonic() function varible.")
    # GPIOの終了処理
    GPIO.cleanup()

'''
モーター初期化処理
'''
# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x70)
myMotor1 = mh.getMotor(1)           # 一つ目のモータの設定
myMotor2 = mh.getMotor(2)           # 二つ目のモータの設定

'''
移動関数 : RCの移動方向と速度をセット
引数 : 移動設定
'''
def motor(direction):
    # direction = 0 前進
    # direction = 1 後進
    # direction = 2 右回転
    # direction = 3 左回転
    # direction = 4 停止
    # run()動作開始
    # setSpeed()モーター速度　制限0~255
    if direction == 0:
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        myMotor1.setSpeed(130)
        myMotor2.setSpeed(130)
        sleep(0.5)

    elif direction == 1:
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        myMotor1.setSpeed(130)
        myMotor2.setSpeed(130)
        sleep(0.5)

    elif direction == 2:
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        myMotor1.setSpeed(130)
        myMotor2.setSpeed(130)
        sleep(0.5)

    elif direction == 3:
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        myMotor1.setSpeed(130)
        myMotor2.setSpeed(130)
        sleep(0.5)

    elif direction == 4:
        # print ("Release")
        myMotor1.run(Adafruit_MotorHAT.RELEASE)
        myMotor2.run(Adafruit_MotorHAT.RELEASE)
        sleep(0.1)

accum_time = 0
curr_fps = 0
fps = "FPS: ??"
prev_time = timer()

# parse options
parser = argparse.ArgumentParser(description='keras-pi.')
parser.add_argument('-m', '--model', default='./model/mnist_deep_model.json')
parser.add_argument('-w', '--weights', default='./model/weights.99.hdf5')
parser.add_argument('-l', '--labels', default='./model/labels.txt')

args = parser.parse_args()

labels = []
with open(args.labels,'r') as f:
    for line in f:
        labels.append(line.rstrip())
print(labels)

model_pred = model_from_json(open(args.model).read())
model_pred.load_weights(args.weights)

# model_pred.summary()

cam = cv2.VideoCapture(0)
count = 0

pred_label = ""

try:
    while True:
        # キー入力
        # getch = _Getch()
        # key = getch()
        key = cv2.waitKey(1) & 0xFF                             # キー入力待ち１ms

        # ラジコン移動
        if key == ord('w'):
            # 後進
            motor(0)
            # motor(4)
            # 距離の取得
            distance = reading(0)
            if distance < 10:
                say(1)
            key = ''
        elif key == ord('z'):
            motor(1)
            # 前進
            # motor(4)
            key = ''
        elif key == ord('d'):
            # 右
            motor(2)
            # motor(4)
            key = ''
        elif key == ord('a'):
            # 左
            motor(3)
            key = ''
        # 's'が押されたら保存
        elif key == ord('s'):
            # 写真を保存
            cv2.imwrite(str(i)+'.jpg',capture)
            i += 1
            print('Save Image...' + str(i) + '.jpg')
            # 音声
            say(0)
            key = ''
        # 'q'が押されたら終了
        elif key == ord('q'):
            capture.release()
            cv2.destroyAllWindows()
            key = ''
            break
        else:
            # 停止
            motor(4)
            key = ''
        

        # start = time.clock()                                    # 開始時刻
        # 画面指定の時のカメラの画像
        # ret, image = capture.read()

        # _, image = capture.read()                               # カメラの画像
        ret, capture = cam.read()                               # カメラの画像
        if not ret:
            print('error')
            break

        count += 1
        if count == 30:
            X = []
            img = capture.copy()
            img = cv2.resize(img, (64, 64))
            img = img_to_array(img)
            X.append(img)
            X = np.asarray(X)
            preds = model_pred.predict(X)

            label_num = 0
            for i in preds[0]:
                if i == 1.0:
                    pred_label = labels[label_num]
                    break
                label_num += 1

            print("label=" + pred_label)
            count = 0
        cv2.rectangle(capture, (0, 30), (50, 17), (0, 0, 0), -1)
        cv2.putText(capture, pred_label, (2, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
        
        # Calculate FPS
        # This computes FPS for everything, not just the model's execution 
        # which may or may not be what you want
        curr_time = timer()
        exec_time = curr_time - prev_time
        prev_time = curr_time
        accum_time = accum_time + exec_time
        curr_fps = curr_fps + 1
        if accum_time > 1:
            accum_time = accum_time - 1
            fps = "FPS: " + str(curr_fps)
            curr_fps = 0
        # Draw FPS
        cv2.rectangle(capture, (0, 0), (50, 17), (0, 0, 0), -1)
        cv2.putText(capture, fps, (2, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

        cv2.imshow('keras-raspi', capture)
        if key == 27: # when ESC key is pressed break
            break



except KeyboardInterrupt:
    # キャプチャの後始末と，ウィンドウをすべて消す
    capture.release()
    cv2.destroyAllWindows()

    myMotor1.run(Adafruit_MotorHAT.RELEASE)
    myMotor2.run(Adafruit_MotorHAT.RELEASE)
    
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()

    capture.release()
    cv2.destroyAllWindows()
