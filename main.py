import time
from umqtt.simple import MQTTClient
import json
import ubinascii
import machine


client_id = 'esp8266-light' + ubinascii.hexlify(machine.unique_id()).decode('utf-8')
command_topic = 'home/woonkamer/tafel/set'
state_topic =   'home/woonkamer/tafel'

network_ssid = 'home'
network_psk  = 'Garuda180'

mqtt_server_ip   = '192.168.1.10'
mqtt_server_port = 1883





def network_start():
    print('starting network')
    import network
    import webrepl
    accesspoint = network.WLAN(network.AP_IF)   
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(network_ssid, network_psk)
    if station.active():
        accesspoint.active(False)
        print('accesspoint mode deactivated')
        print(station.ifconfig())
    webrepl.start()
    print('waiting for connection')
time.sleep(2)





class led_pwm():
    def __init__(self, pin):
        if pin not in (0, 2, 4, 5, 12, 13, 14, 15,):
            raise ValueError ("pin must be 0, 2, 4, 5, 12, 13, 14, or 15")
        self._pwm_device =  machine.PWM(machine.Pin(pin, machine.Pin.OUT), freq = 400, duty = 255)
        self.val = 0
        self._pwm_device.duty(0)
        self.is_on = False

    def value(self, value = None):
        if value == None:
            return self.val
        if  value != max(min(255, value),0):
            raise ValueError ('value must be between 0 and 255')
        if self.val != value:
            self.val = value
            if value == 0:
                self.on = False
            else:
                self.on = True
            self._pwm_device.duty(int(value*255))
        return self.val
        
    def on(self):
        self.value(255)

    def off(self):
        self.value(0)

class led_control():
    def __init__(self):
        self.state = {'brightness': 255,
                     # 'color_temp: None,
                           'color':{'r':0,
                                    'g':0,
                                    'b':0
                                    },
                        # 'effect': effect,
                           'state': 'OFF',
                    # 'transition': None,
                     'white_value': 0
                      }
        self.red_led   = led_pwm(14)
        self.green_led = led_pwm(12)
        self.blue_led  = led_pwm(13)
        self.white_led = led_pwm(15)

    def set_state(self, key, value):
        if self.state[key] != value:
            self.state[key] = value
 
    def update_led(self, state = None):
        if state == None:
            state = self.state
        R = state['color']['r']
        G = state['color']['g']
        B = state['color']['b']
        HSV = RGB_2_HSV((R,G,B))
        R, G, B = HSV_2_RGB((HSV[0],HSV[1],state['brightness']))

        if self.state['state'] == 'ON':
            self.red_led.value(R)
            self.green_led.value(G)
            self.blue_led.value(B)
            self.white_led.value(state['white_value'])

        else:
            self.red_led.value(0)
            self.green_led.value(0)
            self.blue_led.value(0)
            self.white_led.value(0)

        print('led states', 'rgb', (self.red_led.val, self.green_led.val, self.blue_led.val),
          'w', self.white_led.val) 



def RGB_2_HSV(RGB):
    ''' Converts an integer RGB tuple (value range from 0 to 255) to an HSV tuple '''

    # Unpack the tuple for readability
    R, G, B = RGB

    # Compute the H value by finding the maximum of the RGB values
    RGB_Max = max(RGB)
    RGB_Min = min(RGB)

    # Compute the value
    V = RGB_Max;
    if V == 0:
        H = S = 0
        return (H,S,V)


    # Compute the saturation value
    S = 255 * (RGB_Max - RGB_Min) // V

    if S == 0:
        H = 0
        return (H, S, V)

    # Compute the Hue
    if RGB_Max == R:
        H = 0 + 43*(G - B)//(RGB_Max - RGB_Min)
    elif RGB_Max == G:
        H = 85 + 43*(B - R)//(RGB_Max - RGB_Min)
    else: # RGB_MAX == B
        H = 171 + 43*(R - G)//(RGB_Max - RGB_Min)

    return (H, S, V)


def HSV_2_RGB(HSV):
    ''' Converts an integer HSV tuple (value range from 0 to 255) to an RGB tuple '''

    # Unpack the HSV tuple for readability
    H, S, V = HSV

    # Check if the color is Grayscale
    if S == 0:
        R = V
        G = V
        B = V
        return (R, G, B)

    # Make hue 0-5
    region = H // 43;

    # Find remainder part, make it from 0-255
    remainder = (H - (region * 43)) * 6; 

    # Calculate temp vars, doing integer multiplication
    P = (V * (255 - S)) >> 8;
    Q = (V * (255 - ((S * remainder) >> 8))) >> 8;
    T = (V * (255 - ((S * (255 - remainder)) >> 8))) >> 8;


    # Assign temp vars based on color cone region
    if region == 0:
        R = V
        G = T
        B = P

    elif region == 1:
        R = Q; 
        G = V; 
        B = P;

    elif region == 2:
        R = P; 
        G = V; 
        B = T;

    elif region == 3:
        R = P; 
        G = Q; 
        B = V;

    elif region == 4:
        R = T; 
        G = P; 
        B = V;

    else: 
        R = V; 
        G = P; 
        B = Q;


    return (R, G, B)




def mqtt_on_message(topic, msg):
    valid_responses = ('state',
                       'brightness',
                       'color',
                       'white_value'
                       )
    response = json.loads(msg.decode('utf-8'))
    print(topic.decode('utf-8'), response)
    for k, v in response.items():
        if k in valid_response:
            led.set_state(k,v)
    led.update_led()
   

network_start()    
light_client = MQTTClient(client_id, mqtt_server_ip)
light_client.set_callback(mqtt_on_message)
light_client.connect()
light_client.subscribe(command_topic)

led = led_control()

while True:
    light_client.publish(state_topic, json.dumps(led.state),0,True)
    print('return:', led.state)
    light_client.wait_msg()
    time.sleep_ms(100)


