# -*- coding: utf-8 -*-
import cv2
import os
import matplotlib.pyplot as pyplot

if __name__ == '__main__':
    dir_list = os.listdir('image')
    print(str(len(dir_list)) + " files is found \n")

    ###for文内で見つかったファイルを逐次処理
    for i in dir_list:
        ###グレー画像読み込み###
        filename = "image/" + i
        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) #image import
        print("'" + filename +"'" + " is loaded, processing")

        ###グレー画像を保存###
        filename = "gray_image/gray_" + i
        cv2.imwrite(filename, image)
        print("original grayscale image saved >> "+ filename)

        ###ヒストグラフ化、グラフ処理、保存###
        filename = "graph/histgram_" + os.path.splitext(i)[0]+".png"
        print("graph image saved >> "+ filename + "\n")
        hist = cv2.calcHist([image], [0], None, [256], [0,256])
        pyplot.plot(hist)
        pyplot.title(i+" histgram")
        pyplot.xlim(0,256)
        pyplot.savefig(filename)
        pyplot.clf()
