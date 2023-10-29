Reader for PNG images with 7 index colors for use with Pico [Pico e-Paper 5.56](https://www.waveshare.com/wiki/Pico-ePaper-5.65) and Raspberry Pi Pico W.

Once exported to an attachment. Due to lack of memory to run.

# How to use
ePaper is a module https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico-ePaper-5.65f.py with the following Python file saved under the name paper.py. py

After writing to the temporary file, gc is executed. If not executed, it will fail due to lack of memory.

The image is in PNG format, saved in index color with 7 colors. 600x448 size.

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