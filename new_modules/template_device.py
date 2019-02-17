from machine import Pin, PWM
from ujson import loads, dumps
from time import sleep_ms

default_config = {"pin":       0,
                  "inverted":  False,
                  "type":      "binary_sensor",
                  "topic":     "test",
                  "set_topic": "test"
                  }


class input_device():
    def __init__(self, config = default_config):
        if pin not in (0, 4, 5, 12, 13, 14, 15, 16):
            raise ValueError ("pin must be 0, 4, 5, 12, 13, 14, 15 or 16")
        self._sensor   =  Pin(config['pin'], Pin.IN)
        self._last_sens = time()
        self.is_on     = False
        self.value     = 0
        self.old_value = None
        self.state     = 'OFF'  #for most devices should be 'ON' or 'OFF'
        self.old_state = None
        self.type      = config['type']
        self.topic     = config['topic']
        self.set_topic = config['set_topic']

    def __str__(self):
        variables = ( self.type, self.value,  self.is_on, self.old_state,
                      self.state, self._sensor.value(), self._last_sens,
                      elf.topic, self.set_topic)

        log_str = 'type {} value {} is_on {} old_state {} state {}, sensor_val {}, last_sense {} topic {} set_topic {}'
        return(log_str.format(*variables))

    def check_state(self):
        """check_state checks the current state of the binary sensor and
           updates it if the sensor limit has been exceded"""
        pass

    def value(self, val = None):
        return self.value

class output_device():
    def __init__(self, config = defauly_config):
        if pin not in (0, 4, 5, 12, 13, 14, 15, 16):
            raise ValueError ("pin must be 0, 4, 5, 12, 13, 14, 15 or 16")
        self._output   =  Pin(config['pin'], Pin.OUT)
#        self._pwm_device =  PWM(Pin(pin, Pin.OUT), freq = 400, duty = 0)
        self._last_sens = time()
        self.is_on     = False
        self.value     = 0
        self.old_value = None
        self.state     = 'OFF'  #for most devices should be 'ON' or 'OFF'
        self.old_state = None
        self.type      = config['type']
        self.topic     = config['topic']
        self.set_topic = config['set_topic']

    def __str__(self):
        variables = ( self.type, self.value,  self.is_on, self.old_state,
                      self.state, self._sensor.value(), self._last_sens,
                      elf.topic, self.set_topic)

        log_str = 'type {} value {} is_on {} old_state {} state {}, sensor_val {}, last_sense {} topic {} set_topic {}'
        return(log_str.format(*variables))

    def value(self, val = None):
        # depending if this is a pwm device or a regular switch, value is
        # 0-255 or 0-1
        if val in (0,1):
            self._output.value(val)
        return self.value

    def on(self):
        self.value(1)

    def off(self):
        self.value(0)

    def toggle(self):
        if self.val > 0:
            self.value(0)
        else:
            self.value(1)

    def check_state(self):
        """check_state checks the current state of the binary sensor and
           updates it if the sensor limit has been exceded"""
        pass

    def update(self, state):
        if isinstance(state, str):
            state = state.lower() # convert value to lower case
        on_states  = ('true',   'on', True,  1, '1')
        off_states = ('false', 'off', False, 0, '0')
        if state in on_states:
            self.on()
        elif state in off_states:
            self.off()
