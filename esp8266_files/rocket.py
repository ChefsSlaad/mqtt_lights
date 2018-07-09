import time, machine, neopixel
from urandom import getrandbits

colors = { 'red'     : (255,0,0),
           'blue'    : (0,0,255),
           'green'   : (0,255,0),
           'orange'  : (255, 165,0),
           'purple'  : (255,0,255),
           'pink'    : (255,105,180),
           'yellow'  : (255,255,0),
           'white'   : (255,255,255)
         }


class strip():


    def __init__(self, pin = 4, ring = 12, strip = 21):
        self.pixel = neopixel.NeoPixel(machine.Pin(pin), ring+strip)
        self.ring_start  = 0
        self.ring_stop   = ring
        self.strip_start = ring
        self.strip_stop  = strip+ring
        self.ring_range  = range(ring)
        self.strip_range = range(ring, strip+ring)
 
    def _validate_color(self, c):
        c = max( 0, min(255, c)) # make sure color is between 0 and 255
        return c
    
    def set(self, pix, color):
        r, g, b = color
        r = max( 0, min(255, r)) # make sure color is between 0 and 255
        g = max( 0, min(255, g)) # make sure color is between 0 and 255
        b = max( 0, min(255, b)) # make sure color is between 0 and 255
        if 0 <= pix <= self.pixel.n:
            self.pixel[pix] = (r,g,b)
    
    def fixed(self, pixels = None, color = (255,255,255)):
        pixels = self.strip_range if pixels == None else pixels
        for pix in pixels:
            self.pixel[pix] = color
        self.pixel.write()
        
    def dim(self, pix, pct):
        r, g, b = self.pixel[pix]
        if (r, g, b) == 0:
            self.set(pix, (0,0,0))
        elif max(r, g, b) < 10:
            r = max(0, r-1)
            g = max(0, g-1)
            b = max(0, b-1)
            self.set(pix, (r,g,b))
        else:
            self.set(pix,(round(r*pct), round(g*pct), round(b*pct)))

    def clear(self, color = (0,0,0)):
        for pix in len(self.pixel):
            self.pixel[pix] = color
        self.pixel.write()
     
    def chase(self, pixels = None, color = (255,255,255), tail = 5, dim = 0.33, ms_pause = 10, forward = True, loops = 10):

        pixels = self.strip_range if pixels == None else pixels
        done = []
        first = min(pixels)
        last = max(pixels)
        if forward:
            step = 1
            i = first
        else: 
            step = -1
            i = last
        l = 0 # loop count -1 is indefinite
        while loops != l:
            self.set(i, color)
            for j in done:
                self.dim(j, dim)
            done.append(i)
            if len(done) > tail:
                self.set(done.pop(0), (0,0,0))
            self.pixel.write()
            i = i + step
            if i > last:
                i = first
            elif i < first:
                i = last
            if i == first:
                l += 1
            time.sleep_ms(ms_pause)
    
    def kitt(self, pixels = None, color = (255,0,0), loop = 5, ms_pause = 30, tail = 5):
        pixels = self.strip_range if pixels == None else pixels
        l = 0
        while loop != l:
            self.chase(color = color, pixels = pixels, ms_pause = ms_pause, tail = tail, loops = 1, forward = True)
            self.chase(color = color, pixels = pixels, ms_pause = ms_pause, tail = tail, loops = 1, forward = False)
            l += 1
            
    def clear(self):
        for i in range(self.pixel.n):
            self.pixel[i] = (0,0,0)
            self.pixel.write()
            
    def fade_colors(self, color = (255,255,255), dim = 0.95):
        colors = [color]
        while max(color) > 0:
            r, g, b = color
            if max(color) < 20:
                r = max(r - 1, 0)
                g = max(g - 1, 0)
                b = max(b - 1, 0)
            color = (round(r*dim), round(g*dim), round(b*dim))
            colors.append(color)
        return colors

    def fade(self, pixels = None, color = (255,255,255), dim = 0.95, increase = True, ms_pause = 50):
 
        pixels = self.strip_range if pixels == None else pixels
        colors = self.fade_colors(color, dim)
        if increase:
            colors.reverse()
        while len(colors) > 0:
            color = colors.pop()
            for i in pixels :
                self.pixel[i] = color
            self.pixel.write()
            time.sleep_ms(ms_pause)
            
    def starburst(self, pixels = None, color = (0,0,255), dim = 0.80, freq = 0.05, ms_pause = 50, loops = 10):

        pixels = self.strip_range if pixels == None else pixels
        l = 0
        while l != loops * len(pixels):
            for i in pixels:
                if self.pixel[i] == (0,0,0):
                    if freq*100 > getrandbits(7): 
                        self.pixel[i] = color
                else:
                    self.dim(i, dim)
            self.pixel.write()
            time.sleep_ms(ms_pause)
            l += 1

    def fade_in_out(self, pixels = None, color = (0,255,0), loops = 10):
        pixels = self.strip_range if pixels == None else pixels
        l = 0
        while loops != l:
            self.fade(color = color, pixels = pixels, increase = True)
            self.fade(color = color, pixels = pixels, increase = False)    
            l += 1 


    def random_effect(self):
        
        
        r = getrandbits(2)
        i = getrandbits(3)
        c = getrandbits(3)
        
        color = list(colors)[c]
        rgb = colors[color]        
        
        if r == 0:
            target = self.ring_range
            target_name = 'ring'
        else: 
            target = self.strip_range
            target_name = 'band'

        if i == 0:
            print('chase', target_name, color)
            self.chase(pixels = target, color = rgb)
        elif i == 1:
            print('fade_in_out', target_name, color)
            self.fade_in_out(pixels = target, color = rgb)
        elif i == 2:
            print('kitt', target_name, color)
            self.kitt(pixels = target, color = rgb)
        elif i == 3:
            print('starburst', target_name, color)
            self.starburst(pixels = target, color = rgb)
        elif i == 4:
            print('fixed', 'ring', color) #only works for ring
            self.fixed(pixels = self.ring_range, color = rgb)

        else:
            print('clear', 'all')
            self.clear()

               
rocket = strip()

while True:
    rocket.random_effect()
    time.sleep_ms(100)
