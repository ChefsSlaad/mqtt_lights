from machine import Pin, PWM
from ujson import loads, dumps
import rgb_hsv

class led_pwm():
    def __init__(self, pin, topic = None, set_topic = None, inverted = False):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15,):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, or 15")
        self._pwm_device =  PWM(Pin(pin, Pin.OUT), freq = 400, duty = 0)
        self.val         = 0
        self.type        = 'led'
        self.state       = 'OFF'
        self.old_state   = None
        self.topic       = topic
        self.set_topic   = set_topic
        self.inverted    = inverted
        self.is_on       = False
      
        self.value(0)

    def __str__(self):
        
        variables = (self.is_on, self.inverted, self.val, self._pwm_device.duty())
        log_str = 'is_on {}, inverted {}, value {}, duty {}'
        return log_str.format(*variables) 

    def value(self, value = None):
        if value == None:
            return self.val
        elif  value != max(min(255, value),0):
            raise ValueError ('value must be between 0 and 255')
        if self.val != value:
            self.val = value
            if value == 0:
                self.is_on = False
                self.state = 'OFF'
            else:
                self.is_on = True
                self.state = 'ON'
            if self.inverted:
                pin_val = 1023 - int(value*4.01)
            else:
                pin_val = int(value*4.01) 
            self._pwm_device.duty(pin_val)
        return self.val
        
    def update(self, state):
        if isinstance(state, str): 
            state = state.lower() # convert value to lower case
        on_states  = ('true',   'on', True,  1, '1')
        off_states = ('false', 'off', False, 0, '0')
        if state in on_states:
            self.on()
        elif state in off_states:
            self.off()

            
    def on(self):
        self.value(255)

    def off(self):
        self.value(0)
    
    def toggle(self):
        if self.val > 0:
            self.value(0)
        else:
            self.value(255)


class led_strip():
    def __init__(self, pins, topic, set_topic):
        self.type      = 'led_strip'
        self.topic     = topic
        self.set_topic = set_topic
        self.dic_state = {'brightness': 255,
                               'state': 'OFF'
                        # 'transition': None,
                         # 'color_temp: None,
                            # 'effect': effect,
                         }

        if 'red' in pins and 'green' in pins and 'blue' in pins:
            self.red_led   = led_pwm(pins['red'])
            self.green_led = led_pwm(pins['green'])
            self.blue_led  = led_pwm(pins['blue'])
            self.dic_state['color'] = {'r':0, 'g':0, 'b':0 }
 
        if 'white' in pins:
            self.white_led = led_pwm(pins['white'])
            self.dic_state['white_value'] = 0

        self.state     = dumps(self.dic_state)  
        self.old_state = None              
 
    def __str__(self):
       state = self.state
      
       try:
           r = self.red_led.value()
       except AttributeError:
           r = None

       try:
           g = self.green_led.value()
       except AttributeError:
           g = None

       try:
           b = self.blue_led.value()
       except AttributeError:
           b = None

       try:
           w = self.white_led.value()
       except AttributeError:
           w = None

       log_str = 'red {}, green {}, blue {}, white {}, state {}'
       return log_str.format(r, g, b, w, state)      
       
       print('led states', 'rgb', (self.red_led.val, self.green_led.val, self.blue_led.val),
          'w', self.white_led.val) 

    def _set_rgb(self, state):
        
        R = state['color']['r']
        G = state['color']['g']
        B = state['color']['b']
        HSV = rgb_hsv.RGB_2_HSV((R,G,B))
        R, G, B = rgb_hsv.HSV_2_RGB((HSV[0],HSV[1],state['brightness']))
 
        if state['state'] == 'ON':
            self.red_led.value(R)
            self.green_led.value(G)
            self.blue_led.value(B)
 
        else:
            self.red_led.value(0)
            self.green_led.value(0)
            self.blue_led.value(0)
           
    def _update_led(self, state = None):
        if state == None:
            state = self.dic_state
        
        if 'color' in state:
            self._set_rgb(state)
        if 'white_value' in state:
            W = state['white_value']
            if state['state'] == 'ON':
                self.white_led.value(W)
            else:
                self.white_led.value(0)

    def update(self, json_string):
        state = loads(json_string)
        for key, value in state.items():
            if key in ('brightness', 'color', 'state', 'white_value'):
                if self.dic_state[key] != value:
                    self.dic_state[key] = value
        self.state = dumps(self.dic_state)
        print(self.state)
        self._update_led()
        

