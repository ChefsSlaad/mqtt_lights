class binary_sensor():
    def __init__(self, pin, topic, set_topic, invert = True, delay_on = 5, delay_off = 10):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15, 16):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, 15 or 16")
        self._sensor   =  machine.Pin(pin, machine.Pin.IN)
        self._sens_on  = delay_on
        self._sens_off = delay_off
        self._sens_count = 0
        self._old_val  = 0
        self.value     = 0
        self.haschanged = False
        self.is_on     = False
        self.state    = 'OFF'
        self.topic     = topic
        

    def __str__(self):
        variables = ( 
                      self.sensor,
                      self.value,
                      self.is_on,
                      self._old_val,
                      self._sensor.value(),
                      self.haschanged,
                      self._sens_count,
                      self._sens
                     )
        
        log_str = 'sensor: {} value: {} is_on {} old_value {} sensor_state {} has_changed {} sens_count {} sensitivity {}' 
        return(log_str.format(*variables))
         
    def _update_value(self):
        self.value = self._sensor.value()
        self._old_val = self.value
        self.is_on = self.value == 1
        if self.is_on:
            self.state = 'ON'
        else:
            self.state = 'OFF'
        self.message = self.sensor
        
                                       
    def check_state(self):
        self.haschanged = False
        if self._sensor.value() != self._old_val:
            if self.is_on:  # check what value to use as the delay sensitivity 
                sens_limit = self._sens_off
            else:
                sens_limit = self._sens_on

            if self._sens_count < sens_limit:
                self._sens_count += 1
            else:
                self._sens_count = 0
                self._update_value()
                self.haschanged = True
        else:
            self._sens_count = 0    

