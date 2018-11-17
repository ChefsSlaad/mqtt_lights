import unittest
from ujson import loads, dumps

import led_devices

#machine module mocked and installed in ./micropython/lib

led_pin       = 15
led_topic     = 'myledtest'
led_set_topic = 'myledtest/set'

def rgb_to_pins(state):
    R = state['color']['r']
    G = state['color']['g']
    B = state['color']['b']
    HSV = led_devices.rgb_hsv.RGB_2_HSV((R,G,B))
    R, G, B = led_devices.rgb_hsv.HSV_2_RGB((HSV[0],HSV[1],state['brightness']))
    return R, G, B

class led_tests(unittest.TestCase):
    def setUp(self):
        self.single_led = led_devices.led_pwm(pin = led_pin, topic = led_topic, set_topic = led_set_topic)

    def tearDown(self):
        pass

    def test_led_init(self):
        led = self.single_led
        self.assertEqual(led.val, 0, 'led_pwm.val is not 0')
        self.assertEqual(led.type, 'led', 'led_pwm.type is not "led"')
        self.assertEqual(led.state, 'OFF', 'led_pwm.state is not "OFF"')
        self.assertEqual(led.is_on, False, 'led_pwm.is_on is not False')
        self.assertEqual(led.topic, led_topic, 'led_pwm.topic is not correct')
        self.assertEqual(led.set_topic, led_set_topic, 'led_pwm.set_topic is not correct')
        self.assertEqual(led.inverted, False, 'led_pwm.inverted is not False')

    def test_led_print(self):
        expectedstring = "is_on: False, inverted: False, value: 0, duty: 0"
        self.assertEqual(self.single_led.__str__(), expectedstring)

    def test_led_read_value(self):
        v = 0
        self.assertEqual(self.single_led.value(), v, msg='value() does not return {}'.format(v))

    def test_led_set_value(self):
        for v in range(256):
            self.assertEqual(self.single_led.value(v), v, msg='value() does not return {}'.format(v))

    def test_led_inverted(self):
        inv_led = led_devices.led_pwm(pin = led_pin, topic = led_topic, set_topic = led_set_topic, inverted = True)
        self.assertEqual(inv_led.val, 0, 'led_pwm.val is not 0')
        self.assertEqual(inv_led.type, 'led', 'led_pwm.type is not "led"')
        self.assertEqual(inv_led.state, 'OFF', 'led_pwm.state is not "OFF"')
        self.assertEqual(inv_led.is_on, False, 'led_pwm.is_on is not False')
        self.assertEqual(inv_led.inverted, True, 'led_pwm.inverted is not False')
        self.assertEqual(inv_led._pwm_device.duty(), 1023, 'led duty cicle is not at 1023 while inverted and off')

        inv_led.value(255)
        self.assertEqual(inv_led._pwm_device.duty(), 0, 'led duty cicle is not at 0 while inverted and full_on')

    def test_led_pwm_set(self):
        for v in range(256):
            self.single_led.value(v)
            self.assertEqual(self.single_led._pwm_device.duty(), int(round(4.012 * v)))

    def test_led_update(self):
        on_strings = 'on ON 1 On TRUE true'.split()
        off_strings = 'off OFF Off False false FALSE 0'.split()
        for v in on_strings:
            self.single_led.update(v)
            self.assertEqual(self.single_led.state, 'ON')
        for v in off_strings:
            self.single_led.update(v)
            self.assertEqual(self.single_led.state, 'OFF')

    def test_led_on(self):
        self.single_led.on()
        self.assertEqual(self.single_led.state, 'ON', 'led_pwm.state is not "ON"')
        self.assertEqual(self.single_led.is_on, True, 'led_pwm.is_on is not True')


    def test_led_off(self):
        self.single_led.on()
        self.assertEqual(self.single_led.state, 'ON', 'led_pwm.state is not "ON"')
        self.assertEqual(self.single_led.is_on, True, 'led_pwm.is_on is not True')

        self.single_led.off()
        self.assertEqual(self.single_led.value(), 0, 'led_pwm.state is not "OFF"')
        self.assertEqual(self.single_led.state, 'OFF', 'led_pwm.state is not "OFF"')
        self.assertEqual(self.single_led.is_on, False, 'led_pwm.is_on is not False')

    def test_led_toggle(self):
        self.single_led.on()
        self.assertEqual(self.single_led.state, 'ON', 'led_pwm.state is not "ON"')
        self.assertEqual(self.single_led.is_on, True, 'led_pwm.is_on is not True')

        self.single_led.toggle()
        self.assertEqual(self.single_led.value(), 0, 'led_pwm.state is not "OFF"')
        self.assertEqual(self.single_led.state, 'OFF', 'led_pwm.state is not "OFF"')
        self.assertEqual(self.single_led.is_on, False, 'led_pwm.is_on is not False')

        self.single_led.toggle()
        self.assertEqual(self.single_led.value(), 255, 'led_pwm.state is not "OFF"')
        self.assertEqual(self.single_led.state, 'ON', 'led_pwm.state is not "ON"')
        self.assertEqual(self.single_led.is_on, True, 'led_pwm.is_on is not True')

    def test_led_properties(self):
        properties = ((0, 'OFF', False ),
                      (12, 'ON', True ),
                      (24, 'ON', True ),
                      (36, 'ON', True ),
                      (0, 'OFF', False ),
                      (69, 'ON', True ),
                      (199, 'ON', True ),
                      (0, 'OFF', False ),
                      (255, 'ON', True ),
                      (69, 'ON', True ),
                      (69, 'ON', True ),
                     )

        for val, state, ison in properties:
            self.single_led.value(val)
            self.assertEqual(self.single_led.value(), val)
            self.assertEqual(self.single_led.state, state)
            self.assertEqual(self.single_led.is_on, ison)

    def test_out_of_bounds_errors(self):
        pass

class strip_tests(unittest.TestCase):
    def setUp(self):
        rgb  = {'red': 12, 'green': 13, 'blue': 14 }
        ww   = {'white': 15}
        rgbw = {'red': 12, 'green': 13, 'blue': 14 , 'white': 15}
        self.tpc = 'test/strip'
        self.set_tpc = 'test/strip/set'

        self.rgbw = led_devices.led_strip(rgbw, self.tpc, self.set_tpc)
        self.ww = led_devices.led_strip(ww, self.tpc, self.set_tpc)
        self.rgb = led_devices.led_strip(rgb, self.tpc, self.set_tpc)


    def tearDown(self):
        pass

    def test_strip_init_rgb(self):
        strip = self.rgb
        state = {'brightness': 0, 'state':'OFF', 'color': {'r':0,'g':0, 'b':0}}

        self.assertEqual(strip.type, 'led_strip', 'type is not "led_strip"')
        self.assertEqual(strip.dic_state, state, 'state is not correct')
        self.assertEqual(strip.topic, self.tpc, 'topic is not correct')
        self.assertEqual(strip.set_topic, self.set_tpc, 'set_topic is not correct')

    def test_strip_init_w(self):
        strip = self.ww
        state = {'state': 'OFF', 'white_value': 0}
        self.assertEqual(strip.type, 'led_strip', 'type is not "led_strip"')
        self.assertEqual(strip.dic_state, state, 'state is not correct')
#        self.assertEqual(strip.topic, self.tpc, 'led_pwm.topic is not correct')
#        self.assertEqual(strip.set_topic, self.set_tpc, 'set_topic is not correct')

    def test_strip_init_rgbw(self):
        strip = self.rgbw
        state = {'brightness': 0, 'state':'OFF', 'color': {'r':0,'g':0, 'b':0}, 'white_value':0}

        self.assertEqual(strip.type, 'led_strip', 'type is not "led_strip"')
        self.assertEqual(strip.dic_state, state, 'state is not correct')
        self.assertEqual(strip.topic, self.tpc, 'led_pwm.topic is not correct')
        self.assertEqual(strip.set_topic, self.set_tpc, 'set_topic is not correct')

    def test_strip_print(self):
        set_tpc = 'test/strip/set'
        strip_rgb  = self.rgb
        strip_ww   = self.ww
        strip_rgbw = self.rgbw

        str_rgb  = 'red 0, green 0, blue 0, white None, state {"color": {"r": 0, "g": 0, "b": 0}, "brightness": 0, "state": "OFF"}'
        str_rgbw = 'red 0, green 0, blue 0, white 0, state {"color": {"r": 0, "g": 0, "b": 0}, "brightness": 0, "state": "OFF", "white_value": 0}'
        str_ww   = 'red None, green None, blue None, white 0, state {"state": "OFF", "white_value": 0}'

        self.assertEqual(strip_rgb.__str__(),str_rgb)
        self.assertEqual(strip_ww.__str__(),str_ww)
        self.assertEqual(strip_rgbw.__str__(),str_rgbw)

    def test_strip_read_dic_state(self):
        state_rgbw = {'brightness': 0, 'state':'OFF', 'color': {'r':0,'g':0, 'b':0}, 'white_value':0}
        state_ww = {'state':'OFF', 'white_value':0}
        state_rgb = {'brightness': 0, 'state':'OFF', 'color': {'r':0,'g':0, 'b':0}}

        self.assertEqual(self.rgbw.dic_state, state_rgbw)
        self.assertEqual(self.ww.dic_state, state_ww)
        self.assertEqual(self.rgb.dic_state, state_rgb)

    def test_strip_read_state(self):
        state_rgbw = {'brightness': 0, 'state':'OFF', 'color': {'r':0,'g':0, 'b':0}, 'white_value':0}
        state_ww = {'state':'OFF', 'white_value':0}
        state_rgb = {'brightness': 0, 'state':'OFF', 'color': {'r':0,'g':0, 'b':0}}

        self.assertEqual(loads(self.rgbw.state), state_rgbw)
        self.assertEqual(loads(self.ww.state), state_ww)
        self.assertEqual(loads(self.rgb.state), state_rgb)

    def test_strip_update_w(self):
        strip = self.ww
        state = {'state':'ON', 'white_value':0}
        for i in range(1,256):
            state['white_value'] = i
            strip.update(state)
            self.assertEqual(strip.dic_state, state)

    def test_strip_update_rgbw(self):
        pass

    def test_strip_properties(self):
        strip = self.rgbw
        properties = (
            {'state':'OFF', 'white_value':0, 'brightness': 0, 'color': {'r':0,'g':0, 'b':0}},
            {'state':'ON', 'white_value':128, 'brightness': 0, 'color': {'r':0,'g':0, 'b':0}},
            {'state':'ON', 'white_value':128, 'brightness': 100, 'color': {'r':255,'g':0, 'b':0}},
            {'state':'ON', 'white_value':0, 'brightness': 100, 'color': {'r':255,'g':0, 'b':0}},
            {'state':'ON', 'white_value':0, 'brightness': 30, 'color': {'r':255,'g':255, 'b':255}},
            {'state':'OFF', 'white_value':0, 'brightness': 0, 'color': {'r':0,'g':0, 'b':0}},
            {'state':'ON', 'white_value':255, 'brightness': 255, 'color': {'r':255,'g':255, 'b':255}},
            {'state':'OFF', 'white_value':0, 'brightness': 0, 'color': {'r':0,'g':0, 'b':0}}
            )
        for p in properties:
            strip.update(p)
            self.assertEqual(strip.dic_state, p)


    def test__gen_incr(self):
        pass

    def test___next_step(self):
        pass

    def test_strip_update_rgb(self):
        strip = self.rgb
        state = {'state':'ON', 'brightness': 0, 'color': {'r':0,'g':0, 'b':0}}
        colors = (('r', 'g', 'b'), ('g', 'b', 'r'), ('b', 'g', 'r'))
        for color in colors:
            a, b, c = color
            state['color'][a] = 255
            for col2 in range(1,256, 1):
                state['color']['b'] = col2
                for col3 in range(1,256, 2 ):
                    state['color']['c'] = col3
#                    print('testing color {} {} {}'.format(a, col2, col3))
                    for brightness in range(1,256, 3):
                        state['brightness'] = brightness
                        strip.update(state)
                        R, G, B = rgb_to_pins(state)
                        self.assertEqual(strip.dic_state, state)
                        self.assertEqual(strip.red_led.value(), R)
                        self.assertEqual(strip.green_led.value(), G)
                        self.assertEqual(strip.blue_led.value(), B)


    def test_fade(self):
        pass

if __name__ == '__main__':
    unittest.main()
