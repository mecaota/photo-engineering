# -*- coding: utf-8 -*-
import cv2
import os
import matplotlib
import matplotlib.pyplot as pyplot
import numpy as np

if __name__ == '__main__':
    dir_list = os.listdir('image')
    for i in dir_list:
        ###グレー画像読み込み###
        filename = "image/" + i
        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) #image import
        print(filename)

        ###グレー画像を保存###
        filename = "gray_image/gray_" + i
        cv2.imwrite(filename, image)
        print("image list")
        print(filename)

        ###ヒストグラフ化、グラフ処理、保存###
        filename = "graph/histgram_" + i
        print(filename)
        hist = cv2.calcHist([image], [0], None, [256], [0,256])
        pyplot.plot(hist)
        pyplot.title(i+" histgram")
        #pyplot.xlim[0,256]
        pyplot.savefig(filename)
