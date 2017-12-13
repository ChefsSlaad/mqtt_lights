# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import network
import time
from machine import reset

networks = (
    ('BonBini', 'Rabootje'),
    ('home', 'Garuda180'),
    ('marc', 'marcisdabomb')
    )

accesspoint = network.WLAN(network.AP_IF)   
station = network.WLAN(network.STA_IF)
station.active(True)

stations_ssid = (str(net[0],'utf-8') for net in station.scan())


for net in networks:
    ssid, psk = net
    if ssid in stations_ssid:
        station.connect(ssid,psk)
        print('connected to wifi network {}'.format(ssid))
        accesspoint.active(False)



webrepl.start()
gc.collect()

print('waiting to initialize')
for i in range(10):
    print('.', end='')
    time.sleep(0.2)

print()
ips = station.ifconfig()
print(' IP adress {}\n netmask   {} \n gateway   {} \n dns       {}'.format(*ips))
print()    
print('starting main script')

