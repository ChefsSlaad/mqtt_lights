import time
from umqtt.simple import MQTTClient
import ubinascii
import machine


client_id    = 'esp8266-light' + ubinascii.hexlify(machine.unique_id()).decode('utf-8')
esp8266_set  = "home/controller/woonkamer/bank_schemerlamp"
light_set   = "home/woonkamer/bank_schemerlamp/set"
light_topic = "home/woonkamer/bank_schemerlamp"


mqtt_server_ip   = '192.168.1.10'
mqtt_server_port = 1883
retries = 0 #mqtt reconnect retries
max_retries = 86400 #one day


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


def mqtt_check_message():
    try:
        mqtt_client.check_msg()
    except OSError:
        mqtt_connect_and_subscribe()
       

def mqtt_on_message(topic, message):
    tpc = topic.decode('utf-8')
    msg = message.decode('utf-8')
    if tpc == light.tc_set:
        light.update(msg)
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
            mqtt_client.subscribe(light.tc_set)
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
        

light = switch(12, light_topic, light_set)
btn   = machine.Pin(0, machine.Pin.IN)
led   = machine.Pin(13, machine.Pin.OUT)


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

        
mqtt_connect_and_subscribe()

while True:
    mqtt_check_message()
    check_btn_led()
    if light.haschanged:
        mqtt_send_message(light.topic, light.message)
        light.haschanged = False
    print('light  {}   btn    {}, led   {}'.format(light.switch, btn.value(), led.value()))
#    print('micro', micro)
    time.sleep_ms(500)
 
