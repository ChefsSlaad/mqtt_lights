# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network
import time
import ujson
import os


accesspoint = network.WLAN(network.AP_IF)   
station = network.WLAN(network.STA_IF)


def activate_wifi(config_file = 'config.json'):
    config = read_config(config_file)
    networks = ()
    if 'networks' in config:
        networks = config['networks']
    scan_and_connect(networks)

def read_config(config_file = 'config.json'):
    config = {} # some defaults could go here
     
    try:
        if os.stat(config_file).st_size != 0:
            read_file = open(config_file)
            config = ujson.loads(read_file.read())
    except:
        pass
    return config
    
def scan_and_connect(networks = ({'ssid':'test','password':'test'})):
    station.active(True)
    print()
    print('scanning network')
    stations_ssid = []
    while len(stations_ssid) == 0:
        print('.', end='')
        stations_ssid = list(str(net[0],'utf-8') for net in station.scan())
        time.sleep(0.2)
    print()
    print('found networks:', ', '.join(stations_ssid)) 

    for net in networks:
        if 'ssid' in net and 'password' in net:
            ssid = net['ssid'] 
            psk = net['password']
        
            if ssid in stations_ssid:
                station.connect(ssid,psk)
                print('connecting to wifi network {}'.format(ssid))
                print('deactivating accespoint mode')
                accesspoint.active(False)

    print('...getting ip adress')
    ip_adress = '0.0.0.0'
    while ip_adress == '0.0.0.0':
        ip_adress = station.ifconfig()[0]
        time.sleep(0.2)
        print('.', end='')
    print()
    ips = station.ifconfig()
    print(' IP adress {}\n netmask   {} \n gateway   {} \n dns       {}'.format(*ips))
    print()    


activate_wifi()

