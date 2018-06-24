from machine import Pin
import time

class binary_sensor():
    def __init__(self, pin, topic = None, set_topic = None, inverted = False, delay_on = 5, delay_off = 10):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15, 16):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, 15 or 16")
        self._sensor   =  Pin(pin, Pin.IN)
        self._sens_on  = delay_on
        self._sens_off = delay_off
        self._last_sens = time.time()
        self.value     = 0
        self.old_value = None
        self.is_on     = False
        self.type      = 'binary_sensor'
        self.state     = 'OFF'
        self.old_state = None
        self.topic     = topic
        self.set_topic = set_topic

    def __str__(self):
        variables = ( self.type,
                      self.value,
                      self.is_on,
                      self.old_state,
                      self.state,
                      self._sensor.value(),
                      self._last_sens,
                      self.topic,
                      self.set_topic
                     )
        
        log_str = 'type {} value {} is_on {} old_state {} state {}, sensor_val {}, last_sense {} topic {} set_topic {}' 
        return(log_str.format(*variables))
         
    def _update_value(self):
        self.value = self._sensor.value()
        self.is_on = self.value == 1
        if self.is_on:
            self.state = 'ON'
        else:
            self.state = 'OFF'
        self.message = self.sensor
        
                                       
    def check_state(self):
        self.old_state = self.state
        if self.value != self._sensor.value():
            if self.is_on:  # check what value to use as the delay sensitivity 
                sens_limit = self._sens_off
            else:
                sens_limit = self._sens_on

            if self._last_sens + sens_limit < time.time():
                self._update_value()

        else:
            self._last_sens = time.time()    

