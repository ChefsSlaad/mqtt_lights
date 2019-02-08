import time
from ujson import loads, dumps

config  = None
mqtt    = None
device  = None

valid_set_devices = ('led', 'led_strip', 'switch') # these devices have an update() method
valid_input_devices = ('button', 'binary_sensor') # these devices have a check_state() method


def read_config(config_file = None):
    import os
    import ujson
    if config_file == None: #if no file is not specified, read the first config file in the root dir
        config_file = [f for f in sorted(os.listdir()) if f[-5:] == '.json'][0]
    try:
        if os.stat(config_file)[6] != 0:
            print('reading file', config_file)
            with open(config_file) as read_file:
                config = ujson.load(read_file)
    except OSError:
        print('cannto read', config_file)
        config = None
        exit()
    return config

def load_wifi(config):
    import wifi_config
    if 'network' in config:
        networks = config['network']
        wifi_config.scan_and_connect(networks)

def load_mqtt(config, topics):
    import mqtt_client
    # create a list of all the topics to subscribe to (aka command topics)
    name = config['name']
    mqtt_config = config['mqtt_server']
    mqtt = mqtt_client.mqtt_client(topics, name, mqtt_config['server_adress'], callback = mqtt_on_message, debug=mqtt_debug)
    return mqtt


def init_loop(config = None, mqtt = None, device = None):
    config = read_config()
    load_wifi(config)
    device = load_led_strip(config)
    mqtt   = load_mqtt(config, [device.set_topic])
    print(mqtt)
    return mqtt, device, led,

def main_loop(mqtt, device, led):
    active = True
    while active:
        mqtt.publish(device.topic, device.state)
        mqtt.wait_msg()

##blink after message
if __name__ == '__main__':
    mqtt, device, led = init_loop()
