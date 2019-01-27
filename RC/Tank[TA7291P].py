# coding:utf-8
# usbカメラの映像表示
# ラジコン戦車操作
# コマンド　python tank.py 0

# opencv
import cv2
import time

# Rasberry-pi
import RPi.GPIO as GPIO
import curses
from time import sleep


# 顔認識用のファイル
# FACE_CASCADE = './haarcascades/haarcascade_frontalface_alt.xml'     # 顔
# EYE_CASCADE = './haarcascades/haarcascade_frontalface_alt.xml'     # 目
MAIN_CASCADE = './cascade.xml' # 自作(ちっさいマル検出)

# 認識時に小さい画像は認識しない
MIN_SIZE = (30, 30)

Cascade = cv2.CascadeClassifier(MAIN_CASCADE)               # 顔認識用の分類器の生成
capture = cv2.VideoCapture(0)                               # カメラセット

# 画像サイズの指定(指定する場合にのみ使う)
# ret = capture.set(3, 480)
# ret = capture.set(4, 320)

i = 0

# ラジコン初期化処理
# GPIOのポートを指定
L_VREF = 16
L_IN1 = 20
L_IN2 = 21

R_VREF = 13 
R_IN1 = 19
R_IN2 = 26

motor_ports = [
    [L_IN1, L_IN2, L_VREF],
    [R_IN1, R_IN2, R_VREF]
]

GPIO.setmode(GPIO.BCM)
for ports in motor_ports:
    GPIO.setup(ports, GPIO.OUT)

# モーターを制御する関数を定義
def set_motor(pno, job):
    ta_switch = [
        [0, 0], # 停止
        [1, 0], # 時計回り
        [0, 1]] # 反時計回り
    ports = motor_ports[pno]
    sw = ta_switch[job]
    GPIO.output(ports[0], sw[0])
    GPIO.output(ports[1], sw[1])

# モーターを回す
# 回転速度を指定
pwm_l = GPIO.PWM(L_VREF, 5000)
pwm_r = GPIO.PWM(R_VREF, 2500)
pwm_l.start(100)
pwm_r.start(100)


def motor(direction):
    
    # direction = 0 前進
    # direction = 1 後進
    # direction = 2 右
    # direction = 3 左
    # direction = 4 停止
    if direction == 0:
        set_motor(0, 1)
        set_motor(1, 1)
    elif direction == 1:
        set_motor(0, 2)
        set_motor(1, 2)
    elif direction == 2:
        set_motor(0, 2)
        set_motor(1, 1)
    elif direction == 3:
        set_motor(0, 1)
        set_motor(1, 2)
    elif direction == 4:
        set_motor(0, 0)
        set_motor(1, 0)

# キー入力
s = curses.initscr()
curses.noecho()
curses.cbreak()
curses.halfdelay(3)
s.keypad(True)


while True:
    start = time.clock()                                    # 開始時刻
    # 画面指定の時のカメラの画像
    # ret, image = capture.read()

    _, image = capture.read()                               # カメラの画像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    # グレースケールに変換
    # 認識
    faces = Cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=2, minSize=MIN_SIZE)

    key = cv2.waitKey(1) & 0xFF                             # キー入力待ち１ms
    # 's'が押されたら保存
    if key == ord('s'):
        cv2.imwrite(str(i)+'.jpg',image)
        i += 1
        print('Save Image...' + str(i) + '.jpg')
    # 'q'が押されたら終了
    if key == ord('q'):
        capture.release()
        cv2.destroyAllWindows()
        break

    if len(faces):
        continue            # 認識しなかった時

    # 認識した部分に印をつける
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), thickness = 8)
    # 映像処理
    get_image_time = int((time.clock()-start) * 1000)         # 処理時間計測
    # 1フレーム取得するのにかかった時間を表示
    cv2.putText(image, str(get_image_time) + 'ms', (10,10), 1, 1, (255,255,255))
    # 認識した時の画像を保存
    i += 1
    # cv2.imwrite(str(i)+'.jpg',image)
    # print('Save Image...' + str(i) + '.jpg')
    # print('認識しました')
    # time.sleep(3)           # 連続で認識しないように待機、ただし画面も固まる
    # continue               # 待機だと重いのでこっちのほうが良い？あってもなくても変わらん

    cv2.imshow('USB_Camera Test',image)
    # ラジコン
    char = s.getch()
    if key == ord('w'):
        # 前進
        motor(0)

    elif key == ord('z'):
        # 後進
        motor(1)
    elif key == ord('d'):
        # 右
        motor(2)
    elif key == ord('a'):
        # 左
        motor(3)
    else:
        # 停止
        motor(4)
    # sleep(0.7)

# キャプチャの後始末と，ウィンドウをすべて消す
cap.release()
cv2.destroyAllWindows()

GPIO.cleanup()
curses.nocbreak()
screen.keypad(False)
curses.echo()
