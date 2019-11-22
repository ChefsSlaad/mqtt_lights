from machine import Pin, Timer
from time import sleep, sleep_ms, localtime, time
from neopixel import NeoPixel
from onewire import OneWire
from ds18x20 import DS18X20


class multisensor:
    def __init__(self, motion_pin, micro_pin, pixel_pin, pixels, temp_pin):
        self.motion = 'OFF'
        self.motion_timer = Timer(-1)
        self.temp_timer = Timer(-2)
        self.temperature = None
        self.one_wire = DS18X20(OneWire(Pin(temp_pin)))
        self.temp_sensor = None # initiated in function temp_sensor
        self.micro_sensor = Pin(micro_pin, Pin.IN)
        self.micro_sensor.irq(handler = self.micro_high, trigger = Pin.IRQ_RISING)
        self.motion_sensor = Pin(motion_pin, Pin.IN)
        self.motion_sensor.irq(handler = self.motion_high, trigger = Pin.IRQ_RISING)
        self.pixels = NeoPixel(Pin(pixel_pin), pixels)
        self.lastmotion = time()

        self.temp_sensor_init()

    def temp_sensor_init(self):
        self.temp_sensor = self.one_wire.scan()[0]
        sleep_ms(750)
        self.read_temperature()
        self.temp_timer.init(mode = Timer.PERIODIC, period = 10000, callback = self.read_temperature)

    def setcolor(self, color: tuple, pixels: tuple = ()):
        '''set the color of the pixel(s) to a certain color'''
        if pixels == (): pixels = range(self.pixels.n)
        for i in pixels:
            self.pixels[i] = color
        self.pixels.write()

    def read_temperature(self, sensor = None):
        self.one_wire.convert_temp()
        self.temperature = round(self.one_wire.read_temp(self.temp_sensor),1) #read temp and round to 1 digit
        print('{} temperature {}'.format(self.__read_time(), self.temperature))

    def motion_high(self, sensor):
        self.motion = 'ON'
        self.lastmotion = time()
        self.motion_timer.init(mode=Timer.ONE_SHOT, period = 30000, callback = self.sensor_timeout)
        print('{} pir detected. Value {}'.format(self.__read_time(), self.motion))
        self.setcolor((0,255,0))

    def micro_high(self, sensor):
        self.motion = 'ON'
        self.motion_timer.init(mode=Timer.ONE_SHOT, period = 30000, callback = self.sensor_timeout)
        print('{} micro detected. Value {}'.format(self.__read_time(), self.motion))
        self.setcolor((0,0,255))

    def sensor_timeout(self, selftimer):
        self.motion = 'OFF'
        self.setcolor((255,0,0))

    def __read_time(self):
        t = localtime()
        return '{:0<2}:{:0<2}:{:0<2}'.format(t[3],t[4], t[5])


mysensor = multisensor(motion_pin = 4, micro_pin = 15, pixel_pin = 0, pixels = 1, temp_pin = 5)
