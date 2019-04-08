import unittest
from time import time, sleep_ms

import binary_sensor

#machine module mocked and installed in ./micropython/lib

default_config = {"pin":           0,
                  "inverted":      False,
                  "type":          "binary_sensor",
                  "state_topic":   "mytest",
                  "command_topic": "mytest/set",
                  "debug":         False
                  }




class sensor_tests(unittest.TestCase):
    def setUp(self):
        self.sensor = binary_sensor.binary_sensor(default_config)

    def tearDown(self):
        pass

    def test_sensor_init(self):
        sensor = self.sensor
        self.assertEqual(sensor._sens_off, 10, 'sensor off timeout is not 10 secs')
        self.assertEqual(sensor._sens_on, 5, 'sensor off timeout is not 5 secs')
        self.assertEqual(sensor.is_on, False, 'sensor is_on not False')
        self.assertEqual(sensor.value, 0, 'sensor value is not 0')
        self.assertEqual(sensor.old_value, None, 'sensor old_value is not None')
        self.assertEqual(sensor.state, 'OFF', 'sensor state is not OFF')
        self.assertEqual(sensor.old_state, None, 'sensor old_state is not None')
        self.assertEqual(sensor.type, 'binary_sensor', 'sensor type is not binary_sensor')



    def test_sensor_print(self):
        self.sensor._last_sens = 100
        expectedstring = "type binary_sensor value 0 is_on False old_state None state OFF, sensor_val 0, last_sense 100 topic mytest set_topic mytest/set"
        self.assertEqual(self.sensor.__str__(), expectedstring, 'str method does not return expected result')

    def test_sens_check_state(self):
        self.sensor.check_state()
        self.assertEqual(self.sensor.value, 0, 'value should be 0 initially')

    def test_sens_on(self):
        self.sensor.check_state()
        self.assertEqual(self.sensor.value, 0, 'value should be 0 initially')
        self.sensor._sensor.value(1)
        self.sensor.check_state()
        self.assertEqual(self.sensor.value, 0, 'value should be 0 as timeout not over yet')
        sleep_ms(5000)
        self.sensor.check_state()
        self.assertEqual(self.sensor.value, 1, 'value should be 1 as after timeout')
        self.assertEqual(self.sensor.is_on, True)
        self.assertEqual(self.sensor.state, 'ON')

    def test_sens_off(self):
        self.sensor.check_state()
        self.assertEqual(self.sensor.value, 0, 'value should be 0 initially')
        self.sensor._sensor.value(1)
        self.sensor._update_value()
        self.sensor.check_state()
        self.assertEqual(self.sensor.value, 1, 'value should be 1 to start the test')
        self.sensor._sensor.value(0)
        self.sensor.check_state()
        sleep_ms(10000)
        self.sensor.check_state()
        self.assertEqual(self.sensor.value, 0, 'value should be 0 as after timeout')
        self.assertEqual(self.sensor.is_on, False)
        self.assertEqual(self.sensor.state, 'OFF')

    def test_sens_timeout_of_off(self):
        # make the timeout shorter so we can test quicker
        delay = 0.250
        self.sensor._sens_on = delay
        self.sensor._sens_off = delay
        self.sensor.check_state()
        sens_steps = [1,0,1,0,1,0]
        while len(sens_steps) > 0:
            self.sensor.check_state()
            start = time()
            val = sens_steps.pop(0)
            self.sensor._sensor.value(val)
            while start + delay > time() :
                self.sensor.check_state()
                self.assertEqual(self.sensor.value, (1-val))
                sleep_ms(10)
            self.sensor.check_state()
            self.assertEqual(self.sensor.value, val)

if __name__ == '__main__':
    unittest.main()
