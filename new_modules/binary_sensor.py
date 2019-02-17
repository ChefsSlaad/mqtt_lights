from machine import Pin
from time import time, sleep_ms


default_config = {"pin":       0,
                  "inverted":  False,
                  "type":      "binary_sensor",
                  "topic":     "test",
                  "set_topic": "test/set"
                  }


class binary_sensor():
    def __init__(self, config = default_config, timeout_on = 5, timeout_off = 10):
        if config["pin"] not in (0, 4, 5, 12, 13, 14, 15, 16):
            raise ValueError ("pin must be 0, 4, 5, 12, 13, 14, 15 or 16")
        self._sensor   =  Pin(config['pin'], Pin.IN)
        self._last_sens = time()
        self._sens_off = timeout_off
        self._sens_on  = timeout_on
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
                      self.topic, self.set_topic)

        log_str = 'type {} value {} is_on {} old_state {} state {}, sensor_val {}, last_sense {} topic {} set_topic {}'
        return(log_str.format(*variables))

    def _update_value(self):
        self.value = self._sensor.value()
        self.is_on = self.value == 1
        if self.is_on:
            self.state = 'ON'
        else:
            self.state = 'OFF'

    def check_state(self):
        """checkstate checks the current state of the binary sensor and
           updates it if the sensor limit has been exceded"""

        self.old_state = self.state
        if self.value != self._sensor.value():
            if self.is_on:  # check what value to use as the delay sensitivity
                sens_limit = self._sens_off
            else:
                sens_limit = self._sens_on

            if self._last_sens + sens_limit < time():
                self._update_value()

        else:
            self._last_sens = time()
