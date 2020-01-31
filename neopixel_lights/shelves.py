from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

pixel = NeoPixel(Pin(2),60)
light1 = tuple(range(0,12))
light2 = tuple(range(12,24))
light3 = tuple(range(24,36))
light4 = tuple(range(36,48))
light5 = tuple(range(48,60))

lights = (light1, light2, light3, light4, light5)
l1s = (light1, light3, light5)
l2s = (light2, light4)

red     = (255,0,0)
green   = (0,255,0)
blue    = (0,0,255)
black   = (0,0,0)



def colors (pix, color_range, color):
    for i in color_range:
        pix[i] = color
    pix.write()

def christmas():
    while True:
        for l in l1s:
            colors(pixel, l, red)
        for l in l2s:
            colors(pixel, l, green)
        sleep_ms(1000)
        for l in l1s:
            colors(pixel, l, green)
        for l in l2s:
            colors(pixel, l, red)
        sleep_ms(1000)

        
