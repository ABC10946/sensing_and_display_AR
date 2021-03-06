# -*- coding: utf-8 -*-
# https://pongsuke.hatenadiary.jp/entry/2018/04/19/094147

import numpy as np
import cv2
from glob import glob


def main():
    square_size = 1.0      # 正方形のサイズ
    pattern_size = (6, 8)  # 交差ポイントの数
    # チェスボード（X,Y,Z）座標の指定 (Z=0)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    objpoints = []
    imgpoints = []

    for fn in glob("calib/*.jpg"):
        # 画像の取得
        gray = cv2.imread(fn, 0)
        print("loading..." + fn)

        # チェスボードのコーナーを検出
        ret, corner = cv2.findChessboardCorners(gray, pattern_size)
        # コーナーがあれば
        if ret == True:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(gray, corner, (5, 5), (-1, -1), term)
        else:
            print('Chessboard not found!')
            continue
        # appendメソッド：リストの最後に因数のオブジェクトを追加
        imgpoints.append(corner.reshape(-1, 2))
        objpoints.append(pattern_points)
        # corner.reshape(-1, 2) : 検出したコーナーの画像内座標値(x, y)

    # 内部パラメータを計算
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)
    # 計算結果を表示
    print("RMS = ", ret)
    print("mtx = \n", mtx)
    print("dist = ", dist.ravel())
    # 計算結果を保存
    np.savetxt("ret.csv", np.array([ret]), delimiter=',', fmt="%0.14f")
    np.savetxt("mtx.csv", mtx, delimiter=',', fmt="%0.14f")


if __name__ == '__main__':
    main()
