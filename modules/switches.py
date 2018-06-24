from machine import Pin

class switch():
    def __init__ (self, pin, topic = None, set_topic = None, inverted = True):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15, 16):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, 15 or 16")
        self._relay =  Pin(pin, Pin.OUT)
        self.is_on  = False
        self.type = 'switch'
        self.state = 'OFF'
        self.old_state = None
        self.topic  = topic
        self.set_topic = set_topic
        self.inverted = inverted
        self._set_state()

        self.update('OFF')
  
    def __str__(self):
        variables = (self.type, self.state, self.is_on, self._relay.value(), self.topic, self.set_topic)
        log_str = 'type {} state {} is_on {} relay_state {}, topic {}, set_topic {}' 
        return(log_str.format(*variables))

    def _set_state(self):
        if self.is_on:
            state = 1  
        else:
            state = 0  
        
        if self.inverted:
            state = 1 - state
        self._relay.value(state)

    def update(self, value):
        self.old_state = self.state
        on_vals = (True, 1, 'true', 'on')
        off_vals = (False, 0, 'false', 'off')
        if isinstance(value, str): value = value.lower() # convert value to lowercase if it is a string
        if value in on_vals:
            self.is_on  = True
            self.state = 'ON'                   
        if value in off_vals:
            self.is_on  = False
            self.state = 'OFF'
        self._set_state()

    def toggle(self):
        if self.is_on:
            self.update('OFF')
        else:
            self.update('ON')



