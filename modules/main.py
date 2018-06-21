config  = None
devices = []
mqtt = None


def read_config(config_file = 'config.json'):
    import os
    import ujson
    try:
        if os.stat(config_file)[6] != 0:
            print('reading file', config_file)
            with open(config_file) as read_file: 
                config = ujson.load(read_file)
    except OSError:
        print('cannto read', config_file)
        config = None
    return config

def load_wifi(config):
    import wifi_config 
    if 'network' in config:
        networks = config['network']
        wifi_config.scan_and_connect(networks)

def load_mqtt(config, devices):
    import mqtt_client
    # create a list of all the topics to subscribe to (aka command topics)
    all_topics = []
    for dev in devices:
        try:
            all_topics.append(dev.topic_set)
        except AttributeError:
            pass
    name = config['name']
    mqtt_config = config['mqtt_server']
    mqtt = mqtt_client.mqtt_client(all_topics, name, mqtt_config['server_adress'])
            

def load_switch(config, devices):
    import switches
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "switch":
            state_topic = item["state_topic"]
            command_topic = item["command_topic"]
            pin           = item["pin"] 
            invert        = not item["high_on"]
            device = switches.switch(pin, state_topic, command_topic, invert)
            devices.append(device)
    return devices
    
def load_led(config, devices):
    import led_devices
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "led":
            state_topic = item["state_topic"]
            command_topic = item["command_topic"]
            pin           = item["pin"] 
            invert        = not item["high_on"]
            device = led_devices.led_pwm(pin, invert)
            devices.append(device)
    return devices

def load_led_strip(config, devices):
    import led_devices
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "led_strip":
            state_topic = item["state_topic"]
            command_topic = item["command_topic"]
            pin           = item["pin"] 
            device = led_devices.led_strip(pin, state_topic, command_topic)
            devices.append(device)
    return devices

def load_button(config, devices):
    import input_devices
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "button":
            state_topic = item["state_topic"]
            pin           = item["pin"] 
            invert        = not item["high_on"]
            device = input_devices.button(pin, state_topic, invert)
            devices.append(device)
    return devices

def load_sensor(config, devices):
    import input_devices
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "binary_sensor":
            state_topic = item["state_topic"]
            pin           = item["pin"] 
            invert        = not item["high_on"]
            device = input_devices.sensor(pin, state_topic, invert)
            devices.append(device)
    return devices

def load_all(config, devices):
    config = read_config("config.json")
    load_wifi(config)
    load_switch(config, devices)
    load_button(config, devices)
    load_sensor(config, devices)
    load_led(config, devices)
    load_led_strip(config, devices)
    load_mqtt(config, devices)
    return devices



