import machine
import time

class button():
    def __init__(self, pin, press_for_reset = True, inverted = False):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15,):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, or 15")
        self._btn        = machine.Pin(pin, machine.Pin.IN)
        self.ispressed   = False
        self.state       = 'OFF'
        self.topic       = ''
        self.inverted    = inverted
        self.press_time  = 0
        self.lastpress   = time.time()
        self.press_reset = press_for_reset

    def check_state(self):
        value = self.ispressed
        if self.inverted:
            self.ispressed = self._btn.value() == 0
        else:
            self.ispressed = self._btn.value() == 1

        if value != self.ispressed: # i.e. the button has just been pressed
            self.press_time = 0
            self.lastpress = time.time()     
        if self.ispressed:
            self.press_time = time.time() - self.lastpress
        if self.press_time > 5 and self.press_reset:
            machine.reset()
        if self.ispressed:
            self.state = 'ON'
        else:
            self.state = 'OFF'
