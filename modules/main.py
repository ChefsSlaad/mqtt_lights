import wifi_config
import io_devices
import ujson
import os

networks = None
mqtt_config = None
name = None
led_strip = None

def read_config(config_file = 'config.json'):
    config = {} # some defaults could go here
    try:
        if os.stat(config_file).st_size != 0:
            with open(config_file) as read_file: 
                config = ujson.loads(read_file)
    except:
        pass
    return config


def load_config(config_file = 'config.json'):
    config = read_config(config_file)
    # use global variables
    name          = config['name'] if 'name' in config else None
    networks      = config['networks'] if 'networks' in config else None
    mqtt_config   = config['mqtt_server'] if 'mqtt_server' in config else None
    strip_cfg     = config['led_strip'] if 'led_strip' in config else None
    
    led_strip = io_devices.led_strip(strip_cfg['pin'], strip_cfg['state_topic'], strip_cfg['command_topic'])
    




    

