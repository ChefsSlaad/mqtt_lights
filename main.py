import time
from umqtt.simple import MQTTClient
import json
import ubinascii
import machine



network_ssid = 'home'
network_psk  = 'Garuda180'


client_id = 'esp8266-light' + ubinascii.hexlify(machine.unique_id()).decode('utf-8')
state_topic   = 'home/woonkamer/tafel'
command_topic = 'home/woonkamer/tafel/set'


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
        self._pwm_device =  machine.PWM(machine.Pin(pin, machine.Pin.OUT))
        self.val = None
        self.on = False

    def value(self, value = None):
        if value == None:
            return self.val
        if  value != max(min(1, value),0):
            raise ValueError ('value must be between 0 and 1')
        self.val = value
        if value == 0:
            self.on = False
        else:
            self.on = True
        self._pwm_device.duty(int(value*1023))
        return self.val
        
    def on(self):
        self.value(1)

    def off(self):
        self.value(0)
        




class lightstrip():


    def __init__(self, stop = state_topic, ctop = command_topic):
        self.state_topic   = stop
        self.command_topic = ctop
        self.is_on = False
        self.powerstate = 'OFF'
        self.color = (255,255,255)      # r g b
        self.white = 0
        self.brightness = 255
        self.state = None
        s = json.loads(self._write_read())
        print('file content', s)
        self.set_state(s)
#        self.update_state()
#        self.set_state(json.loads(self._write_read()))
#        self._set_led_pins()

        print('state topic:   ', self.state_topic)
        print('command toppic:', self.command_topic)
        print('current state :', self.state) 

        self.light_client = MQTTClient(client_id, mqtt_server_ip)
        print('connected to', mqtt_server_ip, 'as', client_id)
        self.light_client.set_callback(self._mqtt_on_message)
        self.light_client.connect()
        self.light_client.subscribe(self.command_topic)
        
        self._mqtt_publish_state()

        while True:
            self.light_client.wait_msg()
#            print('I got a message')
        

    def _mqtt_on_message(self, topic, msg):
#        print('recieved:  ', topic.decode('utf-8'), msg.decode('utf-8'))
        self.set_state(json.loads(msg.decode('utf-8')))
        self._mqtt_publish_state()
#        time.sleep(1)    

    def _mqtt_publish_state(self):
        self.update_state()
#        print('status msg:', json.dumps(self.state))
        self.light_client.publish(self.state_topic, json.dumps(self.state),0,True)

    # get_state and set_state implement the homeassistant mqtt_jason api
    # see https://home-assistant.io/components/light.mqtt_json/ for more
    # information

    def _write_read(self, str = None):
        response = None
        if str == None:
            f = open('light_state.conf')
            response = f.read()
            print('read', response)
            f.close()
        else:
            f = open('light_state.conf', 'w')
            f.write(str)
            f.close()
        return response    


    def update_state(self):
        self.state = {'brightness':self.brightness,
                    # 'color_temp: None,
                      'color':{'r':self.color[0],
                               'g':self.color[1],
                               'b':self.color[2]
                               },
                    # 'effect': self.effect,
                      'state': self.powerstate,
                    # 'transition': None,
                      'white_value': self.white
                      }
        self._write_read(json.dumps(self.state))

    def set_state(self, payload):
#        print('payload', payload)
        for k, v in payload.items():
            if k == 'state':
                if v == 'ON':
                    self.turn_on()
                else:
                    self.turn_off()
            elif k == 'color':
                self.set_rgb(v)
            elif k == 'brightness':
                self.set_brightness(v)
            elif k == 'white_value':
                self.set_white(v)
            # these parts of the API have not been implemented yet
            elif k == 'color_temp':
                pass
            elif k == 'effect':
                pass
            elif k == 'transition':
                pass

    def turn_on(self):
        self.powerstate = 'ON'
        self.is_on = True
        # turn on controller

    def turn_off(self):
        self.powerstate = 'OFF'
        self.is_on = False
        # turn off controller

    def set_rgb(self, rgb):
        self.color = (rgb['r'],rgb['g'],rgb['b'])
        self._set_led_pins(rgb = (self.color))
        
    def set_white(self, w):
        self.white = w
        self._set_led_pins(white = w)

    def set_brightness(self, level):
        self.brightness = level
        self._set_led_pins(brightness = level)

    def _set_led_pins(self, rgb = None, white = None, brightness = None):
        '''calculate pin values based on rgb, w and brightness values'''
        if rgb == None:
            rgb = self.color
        if white == None:
            white = self.white
        if brightness == None:
            brightness = self.brightness
        # convert the rgb colors 
        hsv = RGB_2_HSV(rgb)
        rgb = HSV_2_RGB((hsv[0], hsv[1], brightness))
        # dim white 
        white = brightness
#        print(rgb, white, brightness)

        pin_red.value(rgb[0]/255)
        pin_green.value(rgb[1]/255)
        pin_blue.value(rgb[2]/255)
        pin_white.value(white/255)

#        print('pin values:','color', rgb, 'white', white, 'brightness', brightness) 


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

    
if __name__ == '__main__':
    pin_red     = led_pwm(14)
    pin_green   = led_pwm(12)
    pin_blue    = led_pwm(13)
    pin_white   = led_pwm(15)


    network_start()    
    light = lightstrip()
 
