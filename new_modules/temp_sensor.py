from time import time
from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20


class temp_sensor():
    def __init__(self, config = {}):
        self._temp_sens = DS18X20(OneWire(Pin(config.get("pin", 0))))
        self._temp_sens_dev = self._temp_sens.scan()[0]
        self.last_read = time()
        self.state = None
        self.old_state = None

        self.type      = config.get('type',"temp_sensor")
        self.topic     = config.get('state_topic', None)
        self.set_topic = config.get('command_topic', None)

        self._temp_sens.convert_temp()

    def __str__(self):
        variables = ( self.type, self.old_state, self.state, self.last_read,
                      self.topic, self.set_topic)

        log_str = 'type {} old_state {} state {}, last_read {} topic {} set_topic {}'
        return(log_str.format(*variables))

    def read_temp(self):
        if time() > self.last_read + 0.750: # needs 750 ms between convert_temp and read_temp
            try:
                self.old_state = self.state
                self.state = str(self._temp_sens.read_temp(self._temp_sens_dev))
                self._temp_sens.convert_temp()
                self.last_read = time()
            except Exception as err:
                print('ran into an error', err)

    def update(self):
        pass

    def check_state(self):
        self.read_temp()
