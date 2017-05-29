# -*- coding: utf-8 -*-
import cv2
import os
import matplotlib
import matplotlib.pyplot as pyplot
import numpy as np

if __name__ == '__main__':
    dir_list = os.listdir('image')
    for i in dir_list:
        ###グレー画像インポート、保存
        image = cv2.imread(i, cv2.IMREAD_GRAYSCALE) #image import
        filename = "gray_image/gray_" + i
        cv2.imwrite(filename, image)
        print("image list")
        print(i)

        ###ヒストグラフ化、グラフ処理、保存
        filename = "graph/histgram_" + i
        hist = cv2.calcHist([image], [0], None, [256], [0,256])
        pyplot.plot(hist)
        pyplot.title(i+" histgram")
        #pyplot.xlim[0,256]
        pyplot.savefig(filename)
