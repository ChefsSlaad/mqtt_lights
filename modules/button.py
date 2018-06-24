from machine import Pin, reset 
from time import time

class button():
    def __init__(self, pin, press_for_reset = True, topic = None, set_topic = None, inverted = False):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15,):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, or 15")
        self._btn        = Pin(pin, Pin.IN)
        self.type        = 'button'
        self.ispressed   = False
        self.state       = 'OFF'
        self.old_state   = None
        self.topic       = topic
        self.set_topic   = set_topic
        self.inverted    = inverted
        self.since_press = time()
        self.press_reset = press_for_reset

    def __str__(self):
        string = 'type {}, pressed {}, state {}, since_press {}, topic {}, set_topic {}'
        return string.format(self.type, self.ispressed, self. state, self.since_press, self.topic, self.set_topic)

    def check_state(self):
        self.old_state = self.state
        if self.inverted:
            self.ispressed = self._btn.value() == 0
        else:
            self.ispressed = self._btn.value() == 1

        if self.state == 'OFF': # i.e. the button has not been pressed
            self.since_press = time()     
        if self.ispressed and self.press_reset:
            if self.since_press + 5 < time():
                reset()
                return
        if self.ispressed:
            self.state = 'ON'
        else:
            self.state = 'OFF'            
