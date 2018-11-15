import unittest
from ujson import loads, dumps

import led_devices

#machine module mocked and installed in ./micropython/lib


class led_tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_led_init(self):
        pass

    def test_led_print(self):
        pass

    def test_led_pwm_set(self):
        pass

    def test_led_properties(self):
        pass

    def test_led_read_value(self):
        pass

    def test_led_set_value(self):
        pass

    def test_led_update(self):
        pass

    def test_led_on(self):
        pass

    def test_led_off(self):
        pass

    def test_led_toggle(self):
        pass

class strip_tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_strip_init_rgb(self):
        pass

    def test_strip_init_w(self):
        pass

    def test_strip_init_rgbw(self):
        pass

    def test_strip_print(self):
        pass

    def test_strip_properties(self):
        pass

    def test_strip_read_value(self):
        pass

    def test_strip_set_value(self):
        pass

    def test_strip_update(self):
        pass

    def test__gen_incr(self):
        pass

    def test___next_step(self):
        pass

    def test_fade(self):
        pass


if __name__ == '__main__':
    unittest.main()
