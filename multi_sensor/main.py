from machine import reset
from time import sleep, localtime
from ntptime import settime
import network



station = network.WLAN(network.STA_IF)
station.active(True)
station.connect('BonBini', 'Rabootje')
ip = '0.0.0.0'
while ip == '0.0.0.0':
    ip = station.ifconfig()[0]
    print('.', end='')
    sleep(0.2)
print('\nconnected using {}'.format(station.ifconfig()[0]))

import tests
