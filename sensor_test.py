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

mqtt_server_ip   = '192.168.1.10'
mqtt_server_port = 1883
retries = 0 #mqtt reconnect retries


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
        self.haschanged = False
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



class sensor():
    def __init__(self,pin, topic, sensitivity = 5):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15, 16):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, 15 or 16")
        self._sensor =  machine.Pin(pin, machine.Pin.IN)
        self._sens = sensitivity
        self._sens_count = 0
        self._old_val = 0
        self.value = 0
        self.haschanged = False
        self.is_on = False
        self.sensor = 'OFF'
        self.message = self.sensor
        self.topic = topic

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
        
    def check_state(self):
        self.haschanged = False
        if self._sensor.value() != self._old_val:
            if self._sens_count < self._sens: 
                self._sens_count += 1
            else:
                self._sens_count = 0
                self._update_value()
                self.haschanged = True
        else:
            self._sens_count = 0


def mqtt_check_message():
    try:
        mqtt_client.check_msg()
    except OSError:
        mqtt_connect_and_subscribe()
       

def mqtt_on_message(topic, message):
    tpc = topic.decode('utf-8')
    msg = message.decode('utf-8')
    for l in lights:
        if tpc == l.tc_set:
            l.update(msg)
    print('topic {}, message {}'.format(tpc, msg))  
    if tpc == esp8266_set and msg == 'RESET':
        machine.reset()

def mqtt_send_message(topic, message):
    tpc = topic.encode('utf-8')
    msg = message.encode('utf-8')
    try:
        mqtt_client.publish(tpc, msg,0,True)
        print('topic {}, message {}'.format(topic, message))  
    except OSError:
        mqtt_connect_and_subscribe()


def mqtt_connect_and_subscribe():
    global mqtt_client
    global retries
    if retries < 300:
        try:
            mqtt_client = MQTTClient(client_id, mqtt_server_ip)
            mqtt_client.connect()
            mqtt_client.set_callback(mqtt_on_message)
            mqtt_client.subscribe(light1.tc_set)
            mqtt_client.subscribe(light2.tc_set)
            mqtt_client.subscribe(esp8266_set)
            print('connected to mqtt server at {}'.format(mqtt_server_ip))
            retries = 0
        except OSError:
            time.sleep(1)
            retries += 1
            print('connection to mqtt server failed, retrying')
            mqtt_connect_and_subscribe() 
    else:
        print('could not connect to mqtt_server at {}'.format(mqtt_server_ip))

        
micro  = sensor(4, micro_topic, sensitivity = 5)
pir    = sensor(5, pir_topic, sensitivity = 5)
light1 = switch(12, light1_topic, light1_set)
light2 = switch(14, light2_topic, light2_set)
lights = (light1, light2)
sensors = (micro, pir, light1, light2)




mqtt_connect_and_subscribe()

while True:
    micro.check_state()
    pir.check_state()
    mqtt_check_message()
    for device in sensors:
        if device.haschanged:
            mqtt_send_message(device.topic, device.message)

    print('microwave  {}   Pir    {}, light1   {},  light2   {}'.format(micro.value, pir.value, light1.switch, light2.switch))
#    print('micro', micro)
    time.sleep_ms(500)
 
