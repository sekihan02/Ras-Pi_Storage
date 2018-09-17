# coding: utf-8
'''
ラズパイでsklearn iris
特徴量2　(本来は４だけど)
クラス２ (本来は3)
'''
import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets, svm
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from sklearn import datasets
# アヤメのデータをロードし、変数に格納
iris_dataset = datasets.load_iris()

# 特徴量のセットをX, ターゲットをyに
X = iris_dataset.data
y = iris_dataset.target
# Xとｙの次元を表示
print(X.shape)          # (150, 4) 150個, 4次元ベクトル
print(y.shape)          # (150,) 150ターゲット
# 特徴量を2つに制限する
X = X[:,:2]
# クラスの２分割
# クラス２のデータを除外する
X = X[y!=2]
y = y[y!=2]

# 分類用にSVMを用意
clf = svm.SVC(C=1.0, kernel='linear')       # リニアは線形　線形サポートベクターマシン
# データの最適化
clf.fit(X,y)

# グラフ描画
