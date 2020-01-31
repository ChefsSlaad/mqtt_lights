import time
from umqtt.simple import MQTTClient
import ubinascii
import machine


client_id    = 'esp8266-light' + ubinascii.hexlify(machine.unique_id()).decode('utf-8')
esp8266_set  = "home/controller/woonkamer/boekenkast"
micro_topic  = "home/woonkamer/boekenkast/sensor/microwave"
pir_topic    = "home/woonkamer/boekenkast/sensor/pir"
light1_set   = "home/woonkamer/boekenkast/light/light1/set"
light1_topic = "home/woonkamer/boekenkast/light/light1"
light2_set   = "home/woonkamer/boekenkast/light/light2/set"
light2_topic = "home/woonkamer/boekenkast/light/light2"

mqtt_server_ip   = '10.0.0.1'
mqtt_server_port = 1883
retries = 0 #mqtt reconnect retries
max_retries = 84600 #one day


class switch():
    def __init__ (self, pin, topic, set_topic):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15, 16):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, 15 or 16")
        self._relay =  machine.Pin(pin, machine.Pin.OUT)
        self.switch = 'OFF'
        self.message = self.switch
        self.is_on  = False
        self.topic  = topic
        self.tc_set = set_topic
        self._set_state()
        self._repeat   = 0
        self._max_rpt  = 1
        self.haschanged = False
  
    def __str__(self):
        variables = ( 
                      self.switch,
                      self.value,
                      self.is_on,
                      self._relay.value()
                      )
        log_str = 'switch: {}, value: {} is_on {} relay_state {}' 
        return(log_str.format(*variables))

    def _set_state(self):
        if self.is_on:
            state = 0  # relay is inverted
        else:
            state = 1  # relay is inverted
        self._relay.value(state)

    def update(self, value):
        on_vals = (True, 1, 'true', 'on')
        off_vals = (False, 0, 'false', 'off')
        if isinstance(value, str): value = value.lower() # convert value to lowercase if it is a string
        if value in on_vals:
            self.is_on  = True
            self.switch = 'ON'                   
        if value in off_vals:
            self.is_on  = False
            self.switch = 'OFF'
        self.message = self.switch
        self._set_state()
        self.haschanged = True 

    def check_state(self):
        if self._repeat >= self._max_rpt:
            self.haschanged = False
            self._repeat = 0
        elif self._repeat < self._max_rpt and self.haschanged:
            self._repeat += 1
        else:
            self.haschanged = False 


class sensor():
    def __init__(self,pin, topic, delay_on = 5, delay_off = 10):
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
        self.sensor    = 'OFF'
        self.message   = self.sensor
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
            self.sensor = 'ON'
        else:
            self.sensor = 'OFF'
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


class mqtt_client():
    def __init__(self, topics, callback, client_id, mqtt_server_ip):
        self.server_ip = mqtt_server_ip
        self.id = client_id
        self.__mqtt_client = MQTTClient(self.id, self.server_ip)
        self.topics = topics
        print(self.topics)  
        self.__callback = callback
        self.connected = False
        self.__connect()
    
    def __connect(self):
        try:
#            print('id', self.id, 'ip' , self.server_ip)
            myclient = MQTTClient(self.id, self.server_ip)
            self.__mqtt_client = MQTTClient(self.id, self.server_ip)
            self.__mqtt_client.set_callback(self.__callback)
            self.__mqtt_client.connect()
            for tpc in self.topics:
                print('subscribing to topic ', tpc)
                self.__mqtt_client.subscribe(tpc)
            print('connected to mqtt server at {}'.format(self.server_ip))            
            self.connected = True
        except OSError:
            print('unable to connect to mqtt server')
            self.connected = False        

    def check_msg(self):
        try:
            self.__mqtt_client.check_msg()
            self.connected = True
        except OSError:
            self.connected = False

    def send_msg(self, topic, message):
        tpc = topic.encode('utf-8')
        msg = message.encode('utf-8')
        try:
            self.__mqtt_client.publish(tpc,msg,0,True)
            print('published topic {}, message {}'.format(topic, message))  
            self.connected = True
        except OSError:
            self.connected = False

    def is_alive(self):
    # check if connected is true and reconnect if it is not. if succesful, the 
    # function will return true, otherwise, false
        if not self.connected:
            self.__connect()
        return self.connected


def mqtt_on_message(topic, message):
    tpc = topic.decode('utf-8')
    msg = message.decode('utf-8')
    for l in lights:
        if tpc == l.tc_set:
            l.update(msg)
    print('topic {}, message {}'.format(tpc, msg))  
    if tpc == esp8266_set and msg == 'RESET':
        machine.reset()


def main_loop():	
    while True:
        if client.is_alive():
            client.check_msg()
            if light.haschanged:
                client.send_msg(light.topic, light.message)
                light.haschanged = False
            print('light  {}   btn    {}, led   {}'.format(light.switch, btn.value(), led.value()))
        time.sleep_ms(500) 


def main_loop():
    while True:
        if client.is_alive():
            client.check_msg()
            for device in sensors:
                device.check_state()
            for device in sensors:
                if device.haschanged:
                    client.send_msg(device.topic, device.message)
        print('microwave {}, inernal_state {}, Pir {}, inernal_state {}, light1   {},  light2   {}'.format(micro.sensor, micro.value,  pir.sensor, pir.value, light1.switch, light2.switch))
#        print('microwave (reported {}, state {}, count {}) Pir (reported {}, state {}, count {}), light1   {},  light2   {}'.format(micro.sensor, micro.value, micro._sens_count, pir.sensor, pir.value, pir._sens_count, light1.switch, light2.switch))
#       print('micro', micro)
        time.sleep_ms(500)


micro  = sensor(4, micro_topic,  delay_on = 10, delay_off = 60)
pir    = sensor(5, pir_topic,  delay_on = 10, delay_off = 60)
light1 = switch(12, light1_topic, light1_set)
light2 = switch(14, light2_topic, light2_set)
lights = (light1, light2)
sensors = (micro, pir, light1, light2)
topics = (light1.tc_set, light2.tc_set, esp8266_set)

client = mqtt_client(topics, mqtt_on_message, client_id, mqtt_server_ip)
main_loop()
