import machine
import time

class led_pwm():
    def __init__(self, pin, inverted = False):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15,):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, or 15")
        self._pwm_device =  machine.PWM(machine.Pin(pin, machine.Pin.OUT), freq = 400, duty = 0)
        self.val         = 0
        self.state       = 'OFF'
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
        self.topic     = topic
        self.set_topic = set_topic
        self.state     = {'brightness': 255,
                               'state': 'OFF'
                        # 'transition': None,
                         # 'color_temp: None,
                            # 'effect': effect,
                         }
                      
        if 'red' in pins and 'green' in pins and 'blue' in pins:
            self.red_led   = led_pwm(pins['red'])
            self.green_led = led_pwm(pins['green'])
            self.blue_led  = led_pwm(pins['blue'])
            self.state['color'] = {'r':0, 'g':0, 'b':0 }
 
        if 'white' in pins:
            self.white_led = led_pwm(pins['white'])
            self.state['white_value'] = 0
 
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
        HSV = RGB_2_HSV((R,G,B))
        R, G, B = HSV_2_RGB((HSV[0],HSV[1],state['brightness']))
 
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
            state = self.state
        
        if 'color' in state:
            self._set_rgb(state)
        if 'white_value' in state:
            W = state['white_value']
            if state['state'] == 'ON':
                self.white_led.value(W)
            else:
                self.white_led.value(0)

    def update(self, state):
        for key, value in state:
            if key in ('brightness', 'color', 'state', 'white_value'):
                if self.state[key] != value:
                    self.state[key] = value
        self._update_led()


def RGB_2_HSV(RGB):
    ''' Converts an integer RGB tuple (value range from 0 to 255) to an HSV tuple '''

    # Unpack the tuple for readability
    R, G, B = RGB

    # Compute the H value by finding the maximum of the RGB values
    RGB_Max = max(RGB)
    RGB_Min = min(RGB)

    # Compute the value
    V = RGB_Max;
    if V == 0:
        H = S = 0
        return (H,S,V)


    # Compute the saturation value
    S = 255 * (RGB_Max - RGB_Min) // V

    if S == 0:
        H = 0
        return (H, S, V)

    # Compute the Hue
    if RGB_Max == R:
        H = 0 + 43*(G - B)//(RGB_Max - RGB_Min)
    elif RGB_Max == G:
        H = 85 + 43*(B - R)//(RGB_Max - RGB_Min)
    else: # RGB_MAX == B
        H = 171 + 43*(R - G)//(RGB_Max - RGB_Min)

    return (H, S, V)


def HSV_2_RGB(HSV):
    ''' Converts an integer HSV tuple (value range from 0 to 255) to an RGB tuple '''

    # Unpack the HSV tuple for readability
    H, S, V = HSV

    # Check if the color is Grayscale
    if S == 0:
        R = V
        G = V
        B = V
        return (R, G, B)

    # Make hue 0-5
    region = H // 43;

    # Find remainder part, make it from 0-255
    remainder = (H - (region * 43)) * 6; 

    # Calculate temp vars, doing integer multiplication
    P = (V * (255 - S)) >> 8;
    Q = (V * (255 - ((S * remainder) >> 8))) >> 8;
    T = (V * (255 - ((S * (255 - remainder)) >> 8))) >> 8;


    # Assign temp vars based on color cone region
    if region == 0:
        return (V, T, P)

    elif region == 1:
        return (Q, V, P)

    elif region == 2:
        return (P, V, T)

    elif region == 3:
        return (P, Q, V)
        
    elif region == 4:
        return (T, P, V)

    else: 
        return (V, P, Q)
