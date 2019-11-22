# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import network
from time import sleep
from machine import reset, Pin

validpins = (0, 2, 4, 5, 12, 13, 14, 15)

networks = (('home', 'Garuda180'),
            ('marc', 'marcisdabomb'))


print('turning off all pins')
for p in validpins:
    pin = Pin(p, Pin.OUT)
    pin.value(0)
    print('pin {} off'.format(p), end=' ')
print()


accesspoint = network.WLAN(network.AP_IF)
station = network.WLAN(network.STA_IF)
station.active(True)

print()
print('scanning network')
stations_ssid = []
while len(stations_ssid) == 0:
    stations_ssid = list(str(net[0],'utf-8') for net in station.scan())
    print('.', end='')
    sleep(0.2)
print('found networks:', ', '.join(stations_ssid))

accesspoint = network.WLAN(network.AP_IF)
station = network.WLAN(network.STA_IF)
station.active(True)

for net in networks:
    ssid, psk = net
    if ssid in stations_ssid:
        station.connect(ssid,psk)
        print('connected to wifi network {}'.format(ssid))
        accesspoint.active(False)

        print('initializing: getting ip adress')
        ip_adress = '0.0.0.0'
        while ip_adress == '0.0.0.0':
            sleep(0.2)
            print('.', end='')
            ip_adress = station.ifconfig()[0]

print()
ips = station.ifconfig()
print(' IP adress {}\n netmask   {} \n gateway   {} \n dns       {}'.format(*ips))
print()
print('starting main script')

print('starting webrepl')
webrepl.start()
print('starting garbage collector')
gc.enable()
gc.collect()
