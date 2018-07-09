import time, machine, neopixel
from urandom import getrandbits

class strip():


    def __init__(self, pin = 4, ring = 12, strip = 21):
        self.pixel = neopixel.NeoPixel(machine.Pin(pin), ring+strip)
        self.ringsize = 12
        self.stripsize = 21
    
 
    def _validate_color(self, c):
        c = max( 0, min(255, c)) # make sure color is between 0 and 255
    
    
    def set(self, pix, color):
        r, g, b = color
        r = max( 0, min(255, r)) # make sure color is between 0 and 255
        g = max( 0, min(255, g)) # make sure color is between 0 and 255
        b = max( 0, min(255, b)) # make sure color is between 0 and 255
        if 0 <= pix <= self.pixel.n:
            self.pixel[pix] = (r,g,b)
        
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
     
    def chase(self, first = 0, last = 11, color = (255,255,255), tail = 5, dim = 0.33, ms_pause = 10, forward = True, loops = -1):
        done = []
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
            if i < first:
                i = last
            if i == 0:
                l += 1
            time.sleep_ms(ms_pause)
    
    def kitt(self, color = (255,0,0), loops = 5, ms_pause = 30, tail = 5):
        l = 0
        while loops != l:
            self.chase(color = color, ms_pause = ms_pause, tail = tail, loops = 1, forward = True)
            self.chase(color = color, ms_pause = ms_pause, tail = tail, loops = 1, forward = False)
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

    def fade(self, start = 0, end = 20, color = (255,255,255), dim = 0.95, increase = True, ms_pause = 50):
        colors = self.fade_colors(color, dim)
        if increase:
            colors.reverse()
        while len(colors) > 0:
            color = colors.pop()
            for i in range(start, end):
                self.pixel[i] = color
            self.pixel.write()
            time.sleep_ms(ms_pause)

    def starburst(self, pixels = range(21), color = (0,0,255), dim = 0.80, freq = 0.05, ms_pause = 50):

        while True:
            for i in pixels:
                if self.pixel[i] == (0,0,0):
                    if freq*100 > getrandbits(7): 
                        self.pixel[i] = color
                else:
                    self.dim(i, dim)
            self.pixel.write()
            time.sleep_ms(ms_pause)
        


    def fade_in_out(self, color = (0,255,0), loops = -1):
        l = 0
        while loops != l:
            self.fade(color = color, increase = True)
            self.fade(color = color, increase = False)    
            l += 1 
             
               
rocket = strip()

rocket.chase()
            
            
            
            
            
    
