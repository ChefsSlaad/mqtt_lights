# tests written for this module

#led devices controls led strips and individual (single color) leds
# there are two classes:
#led_pwm - a basic class to control singe led's; mincluding dimming
#led_strip: a class with multiple led_pwm devices that can be controlled as a led strip
#it includes methods to update strips, as wel as natural dimming and effects
#
from machine import Pin, PWM
from ujson import loads, dumps
from time import time
import rgb_hsv

class led_pwm_simple():
# led_pwm is a basic constructor for

    def __init__(self, config = {}):
        pin = config.get("pin", 0)
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15,):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, or 15")
        self._pwm_device = PWM(Pin(pin, Pin.OUT), freq = 500, duty = 0)
        self.inverted    = config.get("inverted", False)
        self.val         = 0
        self.value(0)

    def value(self, value = None):
        if value == None:
            return self.val
        elif  0 > value > 255:
            raise ValueError ('value must be between 0 and 255')
        self.val = value
        if self.inverted:
            pin_val = 1023 - int(round(value*4.012))
        else:
            pin_val = int(round(value*4.012))
        self._pwm_device.duty(pin_val)
        return self.val


class led_strip():
    def __init__(self, config = {}):
        self.type       = config.get("type", "led_strip")
        self.topic      = config.get("state_topic", "test")
        self.set_topic  = config.get("command_topic", "test/set")
        self.debug      = config.get("debug", False)
        if self.debug:
            from logger import logger
            self.logger = logger()
        else:
            from logger import dummy_logger
            self.logger = dummy_logger()

        self.transition = {'effect': 'fade',
                            'end_state':{},
                                 'step':{},
                      'remaining_steps': 0
                           }
        self.dic_state  = {    'state': 'OFF'
                        # 'transition': None,
                         # 'color_temp: None,
                            # 'effect': effect,
                         }
        pins = config.get("pin")
        if 'red' in pins and 'green' in pins and 'blue' in pins:
            self.red_led   = led_pwm_simple({"pin" : pins['red']})
            self.green_led = led_pwm_simple({"pin" : pins['green']})
            self.blue_led  = led_pwm_simple({"pin" : pins['blue']})
            self.dic_state['color'] = {'r':0, 'g':0, 'b':0 }
            self.dic_state['brightness'] = 0

        if 'white' in pins:
            self.white_led = led_pwm_simple({"pin" : pins['white']})
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

       log_str = 'type {} red {} green {} blue {} white {} state {}'
       return log_str.format(self.type, r, g, b, w, state)

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

    def init_effect(self, end_state, effect = 'fade', steps = 3000):
        # init_effect sets up a color effect (just a fade now) with a end state
        # a step (the difference between end and current devided by the no of steps)
        # and the number of steps remaining.
        self.logger.log('starting effect {} with {} steps'.format(effect, steps))
        transition_step = {}
        if 'brightness' in end_state.keys():
            transition_step['brightness'] = (end_state['brightness'] - self.dic_state['brightness'])/steps
        if 'white_value' in end_state.keys():
            transition_step['white_value'] = (end_state['white_value'] - self.dic_state['white_value'])/steps
        if 'color' in end_state.keys():
            transition_step['color'] = {}
            transition_step['color']['r'] = (end_state['color']['r'] - self.dic_state['color']['r'])/steps
            transition_step['color']['g'] = (end_state['color']['g'] - self.dic_state['color']['g'])/steps
            transition_step['color']['b'] = (end_state['color']['b'] - self.dic_state['color']['b'])/steps
        self.transition['end_state'] = end_state
        self.transition['step'] = transition_step
        self.transition['remaining_steps'] = steps
        self.transition['end_time'] = round(time() + (steps / 10))
        self.logger.log('transition effect', dumps(self.transition))

    def stop_transition(self):
        self.transition['remaining_steps'] = 0

    def next_step(self):
        # push the effect one step allong and update the effect
        transition = self.transition
        end_state = self.transition['end_state']
        step = self.transition['step']
        remaining_steps = self.transition['remaining_steps']
        next_state = {}
        if 'brightness' in end_state.keys():
            next_state['brightness'] = round(end_state['brightness'] - step['brightness']*remaining_steps)
        if 'white_value' in end_state.keys():
            next_state['white_value'] = round(end_state['white_value'] - step['white_value']*remaining_steps)
        if 'color' in end_state.keys():
            next_state['color'] = {}
            next_state['color']['r'] = round(end_state['color']['r'] - step['color']['r']*remaining_steps)
            next_state['color']['g'] = round(end_state['color']['g'] - step['color']['g']*remaining_steps)
            next_state['color']['b'] = round(end_state['color']['b'] - step['color']['b']*remaining_steps)
        next_state['state'] = "ON" # any effect only makes sense if the trip is on
        self.update(next_state)
        self.logger.log('effect step {}'.format(remaining_steps), dumps(next_state))

    def time_to_steps_remaining(self, now = None):
        if now == None:
            now = time()
        remaining_time = self.transition['end_time'] - now
        return max(0, round(remaining_time*10))

    def check_state(self):
        self.old_state = self.state
        if self.transition['remaining_steps'] > 0:
            self.transition['remaining_steps'] = self.time_to_steps_remaining()
            self.next_step()

    def update(self, update_state):
        # check if state is a dict, then check if it is a json string
        # in invalid, exit the function
        if isinstance(update_state, dict):
            state = update_state
        elif isinstance(update_state, str):
            try:
                state = loads(update_state)
            except ValueError:
                return
        self.logger.log('updating led strip with state', dumps(state))
        if "transition" in state.keys():
            print(state)
            self.init_effect(state, state["effect"], state["transition"]*10)
            self.update({'state':'ON'})
            return
        for key, value in state.items():
            self.dic_state[key] = value
        self.state = dumps(self.dic_state)
        self._update_led()
