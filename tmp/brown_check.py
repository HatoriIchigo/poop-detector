#!/usr/bin/env python3
"""茶色検出の閾値確認用。3秒ごとに撮影して、茶色の割合を永遠にprintする。

起動時の1枚目を「空の便器」のベースラインとして使い、以降は差分のあった領域のうち
茶色の割合を出す。閾値は下の定数を書き換えて調整する。Ctrl+Cで終了。
"""
import time

import cv2
import numpy as np
from picamera2 import Picamera2

INTERVAL = 3  # 秒
# OpenCVのHSVは H:0-179, S:0-255, V:0-255
HSV_LO = (5, 60, 20)
HSV_HI = (25, 255, 200)
DIFF_TH = 30  # 差分の二値化閾値
ROI = None  # 判定範囲 (x, y, w, h)。Noneなら全体

cam = Picamera2()
cam.configure(cam.create_still_configuration(main={"size": (1280, 720), "format": "RGB888"}))
cam.start()
time.sleep(1)  # 露出安定待ち


def capture():
    # "RGB888" はnumpy上ではBGR並びなのでOpenCVにそのまま使える
    frame = cam.capture_array()
    if ROI:
        x, y, w, h = ROI
        frame = frame[y : y + h, x : x + w]
    return cv2.GaussianBlur(frame, (5, 5), 0)


baseline = capture()
print("ベースラインを取得しました（空の状態にしておく）")

for i in range(1000000):
    frame = capture()

    brown = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), np.array(HSV_LO), np.array(HSV_HI))
    diff = cv2.absdiff(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY))
    change = cv2.inRange(diff, DIFF_TH, 255)
    target = cv2.bitwise_and(brown, change)

    change_px = cv2.countNonZero(change)
    change_ratio = change_px / change.size
    brown_ratio = cv2.countNonZero(target) / change_px if change_px else 0.0
    print(f"{time.strftime('%H:%M:%S')}  変化領域={change_ratio:.3f}  茶色割合={brown_ratio:.3f}")

    # 何に反応したか目で確認できるように、判定領域を赤くした画像を上書き保存する
    view = frame.copy()
    view[target > 0] = (0, 0, 255)
    cv2.imwrite("latest.png", view)

    time.sleep(INTERVAL)
