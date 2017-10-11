# -*- coding: utf-8 -*-
# 変更点：0人になったときに画像ではなくテキストを表示するようにした
import dbReaderWriter
import os
from PIL import Image, ImageDraw, ImageFont



yoko = 1500         #サイズの設定。ここの数字を変えるだけで縦のサイズ、文字のサイズなどがすべて最適化される
tate = int(yoko/3*2)

canvas = Image.new('RGB', (yoko,tate ), (53,122,68))     #背景の設定（rgb,サイズ,rgbの値）
draw = ImageDraw.Draw(canvas)      #背景の描画

canvas_left = Image.new('RGB', ((int)(yoko/5*2), (int)(tate/20*17)), (42,147,203))     #左ブロックの設定（rgb,座標,rgbの値）
canvas.paste(canvas_left, ((int)(yoko/15), (int)(tate/10)))         #左ブロックの描画 

canvas_right = Image.new('RGB', ((int)(yoko/5*2),(int)(tate/20*17)), (234,145,28))     #右ブロックの設定（rgb,座標,rgbの値）
canvas.paste(canvas_right, ((int)(yoko/15*8), (int)(tate/10)))          #右ブロックの描画


font = ImageFont.truetype('C:\Windows\Fonts\msgothic', int(tate/100*9))      #在室・学内フォントの設定（使用するパスの場所,サイズ）
draw.text((int(yoko/5), int(tate/100)), u'在室　　　　　　学内', font=font, fill='#FFF')      #在室・学内の描画（座標, テキスト,　フォント, 色）

font = ImageFont.truetype('C:\Windows\Fonts\msgothic', int(tate/100*8))     #メンバーのフォントの設定

rw=dbReaderWriter.ReaderWriter()
rw.ConnectToDB()

Fill = '#000'       #メンバーのフォントの色の指定

zaisitu=rw.GetZaishituUsers()       #在室しているメンバーの取得
zaisitumem = 0           #在室メンバーの数を数える変数
for row in zaisitu:      #メンバーの数を数えるループ
    zaisitumem+= 1

gakunai=rw.GetGakunaiUsers()        #学内にいるメンバーの取得
gakunaimem = 0           #学内メンバーの数を数える変数
for row in zaisitu:      #メンバーの数を数えるループ
    gakunaimem+= 1


if zaisitumem & gakunaimem == 0:
    os.system('./upload.sh 0')

else:
    zaisitu=rw.GetZaishituUsers()       #在室しているメンバーの取得
    i = tate/250*3          #表示するメンバーの縦座標の調整をする変数
    j = 0                   #行の数をカウントする変数
    for row in zaisitu:
        if zaisitumem <= 8:          #8人以内なら
            draw.text((int(yoko/150*31), int(tate/100*i)), row[0], font=font, fill=Fill)        #在室メンバーの表示（座標,テキスト,フォント,色）
            i += tate/100   
        else:               #9人以上なら
            if j%2 == 0:    #偶数列の表示
                draw.text((int(yoko/150*12), int(tate/100*i)), row[0], font=font, fill=Fill)        #在室メンバーの表示（座標,テキスト,フォント,色）

            else:           #奇数列の表示
                draw.text((int(yoko/150*40), int(tate/100*i)), row[0], font=font, fill=Fill)        #在室メンバーの表示（座標,テキスト,フォント,色）
                i += tate/100 
            j += 1


    gakunai=rw.GetGakunaiUsers()        #学内にいるメンバーの取得
    i = tate/250*3          #表示するメンバーの縦座標の調整をする変数
    j = 0                   #列を判別する変数、偶数なら左、奇数なら右とする
    i = tate/250*3
    for row in gakunai:
        if gakunaimem <= 8:          #8人以内なら
            draw.text((int(yoko/150*103), int(tate/100*i)), row[0], font=font, fill=Fill)        #学内メンバーの表示（座標,テキスト,フォント,色）
            i += tate/100   
        else:               #9人以上なら
            if j%2 == 0:    #左の列の表示
                draw.text((int(yoko/150*82), int(tate/100*i)), row[0], font=font, fill=Fill)        #学内メンバーの表示（座標,テキスト,フォント,色））

            else:           #右の列の表示
                draw.text((int(yoko/150*112), int(tate/100*i)), row[0], font=font, fill=Fill)        #学内メンバーの表示（座標,テキスト,フォント,色）
                i += tate/100 
            j += 1


    canvas.save(u'C:\\Users\sldl77\Pictures\slackbot.jpg', 'JPEG', quality=100, optimize=True)         #パスの場所に画像を保存 

    os.system('./upload.sh 1')
