import time
from umqtt.simple import MQTTClient
import ubinascii
import machine


client_id    = 'esp8266-light' + ubinascii.hexlify(machine.unique_id()).decode('utf-8')
esp8266_set  = "home/controller/woonkamer/schemerlamp"
light_set   = "home/woonkamer/bank_schemerlamp/set"
light_topic = "home/woonkamer/bank_schemerlamp"

mqtt_server_ip   = '10.0.0.1'
mqtt_server_port = 1883
retries = 0 #mqtt reconnect retries
max_retries = 86400 #time 

## sonoff GPIO pins
# PIN 12-----------------replay

# PIN 13-----------------LED

# PIN 0------------Button


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
                      self._relay.value,
                      self.is_on,
                      self._relay.value()
                      )
        log_str = 'switch: {}, value: {} is_on {} relay_state {}' 
        return(log_str.format(*variables))

    def _set_state(self):
        if self.is_on:
            state = 1  # relay is inverted
        else:
            state = 0  # relay is inverted
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

    def toggle(self):
        if self.is_on:
            self.update('OFF')
        else:
            self.update('ON')


       

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
    if tpc == light.tc_set:
        light.update(msg)
    print('topic {}, message {}'.format(tpc, msg))  
    if tpc == esp8266_set and msg == 'RESET':
        machine.reset()


def check_btn_led():
    led.value(1) # led is inverted
    if light.is_on:
        led.value(0)
    d = 0
    duration = 300
    while btn.value() == 0: # button is inverted
        l = led.value()
        d += duration
        led.value(1-l) # toggle led
        time.sleep_ms(duration)
        if d > 5000:
            machine.reset()
    if d > 0:
        light.toggle()

def main_loop():	
    while True:
        check_btn_led()
        if client.is_alive():
            client.check_msg()
            if light.haschanged:
                client.send_msg(light.topic, light.message)
                light.haschanged = False
            print('light  {}   btn    {}, led   {}'.format(light.switch, btn.value(), led.value()))
        time.sleep_ms(500) 

light = switch(12, light_topic, light_set)
btn   = machine.Pin(0, machine.Pin.IN)
led   = machine.Pin(13, machine.Pin.OUT)
client = mqtt_client((light.tc_set, esp8266_set),mqtt_on_message, client_id, mqtt_server_ip)

main_loop()
