from machine import Pin, PWM

led_default = {"pin":           0,
               "inverted":      False,
               "type":          "led",
               "state_topic":   "test",
               "command_topic": "test/set",
               "debug":          False
               }

class led_pwm():
# led_pwm is a basic constructor for

    def __init__(self, config = {}):
        pin = config.get("pin", 0)
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15,):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, or 15")
        self._pwm_device = PWM(Pin(pin, Pin.OUT), freq = 500, duty = 0)
        self.inverted    = config.get("inverted", False)
        self.is_on       = False
        self.val         = 0
        self.state       = 'OFF'
        self.old_state   = None
        self.type        = config.get("type", "led")
        self.topic       = config.get("state_topic", None)
        self.set_topic   = config.get("command_topic", None)

        self.value(0)

    def __str__(self):
        variables = (self.is_on, self.inverted, self.val, self._pwm_device.duty())
        log_str = 'is_on: {}, inverted: {}, value: {}, duty: {}'
        return log_str.format(*variables)

    def value(self, value = None):
        if value == None:
            return self.val
        elif  0 > value > 255:
            raise ValueError ('value must be between 0 and 255')
        self.val = value
        if value == 0:
            self.is_on = False
            self.state = 'OFF'
        else:
            self.is_on = True
            self.state = 'ON'
        if self.inverted:
            pin_val = 1023 - int(round(value*4.012))
        else:
            pin_val = int(round(value*4.012))
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

    def check_state(self):
        pass

    def on(self):
        self.value(255)

    def off(self):
        self.value(0)

    def toggle(self):
        if self.is_on:
            self.value(0)
        else:
            self.value(255)
