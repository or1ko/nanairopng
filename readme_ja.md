
[Pico e-Paper 5.56](https://www.waveshare.com/wiki/Pico-ePaper-5.65) と [Raspberry Pi Pico W]()での利用を
想定した7色のインデックスカラーのPNG画像のリーダー。

一度添付ファイルに書き出す。
メモリが不足して実行できないので

# 利用方法

epaperは下記のPythonファイルをepaper.pyという名前で保存したモジュール
https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico-ePaper-5.65f.py

一時ファイルに書き出し後に、gcを実行する。
実行しないとメモリ不足で失敗する

画像は、7色でインデックスカラーで保存されたPNG形式の画像。
600x448サイズ。

```python
from epaper import EPD_5in65
from nanairopng import Png

png_file = 'raspi.png'

color_map = [
    0x00 # Black
    ,0x01 # White
    ,0x02 # Green
    ,0x03 # Blue
    ,0x04 # Red
    ,0x05 # Yellow
    ,0x06 # Orange
]

print(png_file)

tmpfile = 'png.tmp'
png = Png(png_file)
with open(tmpfile, 'wb') as output:
    png.convertAndWrite(output, color_map)

width, height = png.readDimensions()

import gc
gc.collect()
alloc = gc.mem_alloc()
free = gc.mem_free()

epd = EPD_5in65()
epd.fill(0xff)

with open(tmpfile, "rb") as png:
    for y in range(0, height):
        row = png.read(width)
        for x in range(0, len(row)):
            epd.pixel(x,y,row[x])

epd.EPD_5IN65F_Display(epd.buffer) 
```