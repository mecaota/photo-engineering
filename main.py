# -*- coding: utf-8 -*-
import cv2
import os
import json
import matplotlib.pyplot as pyplot
png = ".png"

###コンソールに横線出力###
def print_line():
    print("--------------------------------------------------------------------")

###ディレクトリパス生成###
def create_path(dirname, filename, fileex):
    return dirname + filename + fileex

###画像読み込み(opencvで読めないファイルはValueError吐く)###
def load_image(path):
    #グレースケール画像として読み込み
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("'" + path +"'" + "はこのプログラムでは扱えないファイルです。このファイルはパスされます。")
    print("'" + path +"'" + "が読み込まれました。処理中です。")
    #opencv型イメージを返す
    return image

###画像保存(グレー,2値)###
def save_image(image, type, filename):
    #セーブするファイルの種別判別
    if type == "gray":
        word = "グレースケール"
        pathfraze = "gray_image/gray_"
        fileex = png
    elif type == "binary":
        word = "2値"
        pathfraze = "binary_image/binary_"
        fileex = png
    else:
        print("Error:" + type +"画像保存処理でエラーが発生しました。")
        return 0
    path = create_path(pathfraze, filename, fileex)
    #画像を保存
    cv2.imwrite(path, image)
    print(word + "化したオリジナル画像が保存されました >> "+ path)

###json保存###
def save_json(data, path):
    with open(path,'w') as f:
        json.dump(data, f, indent='\t')
        print("jsonが"+str(path)+"に保存されました\n")

###jsonロード###
def load_json(path):
    with open(path,'r') as f:
        return json.load(f)

###ヒストグラム生成##
def create_graph(hist, filename):
    path = create_path("graph/histgram_", filename, png)
    pyplot.plot(hist)
    pyplot.title(i+" histgram")
    pyplot.xlim(0,256)
    pyplot.savefig(path)
    pyplot.clf()
    print("グラフ画像が保存されました >> "+ path+"\n")

###閾値算出###
def compare_pixelsize(hist, image_size, history, file):
    #過去処理履歴内の２値化時背景割合データを参照。なければ50で初期化
    inp = 50
    if(file in history):
        inp = int(history[file])
        print("過去に2値化する際の基準画像の面積比として、"+str(inp)+"%で処理した履歴があります。このまま処理する場合はエンターを押してください")
    else:
        history.update({file:'50'})
        print("2値化する際の基準画像の面積比を0-100の範囲内で入力してください。入力がない場合は自動的に50として処理します")
    
    #閾値決定用の面積比受付
    try:
        inp = int(input("(0-100)% >>>"))
    except ValueError:
        if(inp):
            pass
        else:
            print("エラー：入力値が不正です")
    history[file] = inp
    print(str(history[file]) + "を面積比として処理します")
    comp = image_size//100*inp
    cal = 0
    for i in range(hist.size):
        cal = cal + hist[i]
        if(comp < cal):
            print("閾値：" +str(i) + "\n")
            return i, history

###2値画像生成###
def create_binaryimage(image, thresh):
    ret, binary_image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
    return binary_image

###メイン###
if __name__ == '__main__':
    #過去の処理履歴を参照
    try:
        history = load_json("comp_hist.json")
    except:
        history = {}
        pass
    #imageフォルダ内ファイルリストを読み込み
    dir_list = os.listdir('input')
    print("inputフォルダ内から " + str(len(dir_list)) + " ファイルが見つかりました。")
    print_line()
    #接続成分保存用の辞書型オブジェクトを宣言
    connect_count = {}

    #for文内で見つかったファイルを逐次処理
    for i in dir_list:
        #画像ディレクトリ読み込み
        filename = os.path.splitext(i)[0]
        fileex = os.path.splitext(i)[1]
        #画像読み込み・保存
        try:
            #グレースケール画像として読み込み
            path = create_path("input/", filename, fileex)
            image = load_image(path)
            save_image(image, "gray", filename)
        except ValueError as e:
            print(e)
            print_line()
            continue
        #ヒストグラム計算
        hist = cv2.calcHist([image], [0], None, [256], [0,256])
        #グラフ処理・保存
        create_graph(hist, filename)
        #2値化処理・保存
        thresh, history = compare_pixelsize(hist, image.size, history, filename+fileex)
        binary_image = create_binaryimage(image, thresh)
        save_image(binary_image, "binary", filename)
        #連結成分ラベリング＆数え上げ
        pixelsum = cv2.connectedComponents(binary_image)[0]
        print("連結成分個数："+str(pixelsum))
        connect_count[i] = pixelsum
        print_line()
    save_json(history,"comp_hist.json")
    save_json(connect_count, "connect_count.json")
    print("Program finished"+"\n")