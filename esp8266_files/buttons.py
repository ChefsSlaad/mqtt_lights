import neopixel
from machine import Pin
from time import sleep_ms
from urandom import getrandbits


colors = { 'red'     : (255,0,0),
           'orange'  : (255, 165,0),
#           'yellow'  : (255,255,0),
           'green'   : (0,255,0),
           'turquois': (0,255,255),
           'blue'    : (0,0,255),
           'purple'  : (255,0,255),
#           'pink'    : (255,105,180),
           'white'   : (255,255,255)
         }

color_names = ('red', 'orange', 'green', 'turquois', 'blue', 'purple', 'white')
print(color_names)


pixels = neopixel.NeoPixel(Pin(5),4)
btn_colors =[]
for i in range(pixels.n):
    btn_colors.append(i)
    pixels[i] = colors[color_names[i]]
pixels.write()


def setup_btns():
    btns = []
    for i in (15,13,12,14): #the button pins
        btn = Pin(i, Pin.IN)
        btns.append(btn)
#        btn.irq(trigger = Pin.IRQ_RISING, handler = btn_pressed)
    return btns

#effects:
# next color
# rainbow
# chase
# random

def next_effect(pixels, i):
    global btn_colors
    next_color = (btn_colors[i] +1) % len(color_names) # loop to the next color
    btn_colors[i] = next_color
    print('button {} pressed. colors {}'.format(i, btn_colors))
    if next_color == 0: #color range reached
        random_colors(pixels)
    elif all(x == btn_colors[0] for x in btn_colors):
        rainbow(pixels)
    else:
        pixels[i] = colors[color_names[next_color]]
        pixels.write()

def rainbow(pixels):
    global btn_colors
    length = pixels.n
    for c in range(len(color_names)-1,-1,-1):
        for i in range(length):
            pixels[i] = colors[color_names[c]]
            btn_colors[i] = c
            pixels.write()
            sleep_ms(100)


def random_colors(pixels):
        global btn_colors
        for r in range(40):
            i = getrandbits(8) % pixels.n
            newcolorid = getrandbits(8) % len(color_names)
            pixels[i] = colors[color_names[newcolorid]]
            btn_colors[i] = newcolorid
            pixels.write()
            sleep_ms(100)

def main_loop(btns, pixels, colors):
    old_btn_vals = [btn.value() for btn in btns]
    while True:
        for i in range(4):
            sleep_ms(20)
            if (btns[i].value() == 1) and (btns[i].value() != old_btn_vals[i]):
                next_effect(pixels, i)
            old_btn_vals[i] = btns[i].value()

btns = setup_btns()
main_loop(btns, pixels, colors)
