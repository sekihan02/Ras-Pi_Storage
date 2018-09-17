# coding: utf-8
'''
usbカメラで顔認識
1.認識出来たら画面を保存
2.キー's'で保存
3.'q'で終了
'''
import cv2
import time

# 顔認識用のファイル
FACE_CASCADE = './haarcascades/haarcascade_frontalface_alt.xml'     # 顔
# EYE_CASCADE = './haarcascades/haarcascade_frontalface_alt.xml'     # 目

# 認識時に小さい画像は認識しない
MIN_SIZE = (30, 30)

Cascade = cv2.CascadeClassifier(FACE_CASCADE)               # 顔認識用の分類器の生成
capture = cv2.VideoCapture(0)                               # カメラセット

# 画像サイズの指定(指定する場合にのみ使う)
# ret = capture.set(3, 480)
# ret = capture.set(4, 320)

i = 0
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
    cv2.imwrite(str(i)+'.jpg',image)
    print('Save Image...' + str(i) + '.jpg')
    print('認識しました')
    time.sleep(3)           # 連続で認識しないように待機、ただし画面も固まる
    # continue               # 待機だと重いのでこっちのほうが良い？あってもなくても変わらん

    cv2.imshow('USB_Camera Test',image)

# キャプチャの後始末と，ウィンドウをすべて消す
cap.release()
cv2.destroyAllWindows()
