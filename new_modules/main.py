import time
from ujson import loads

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
    mqtt = mqtt_client.mqtt_client(topics, name, mqtt_config['server_adress'], callback = mqtt_on_message, debug=True)
    return mqtt

def load_led_strip(config):
    import led_devices
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "led_strip":
            state_topic = item["state_topic"]
            command_topic = item["command_topic"]
            pin           = item["pin"]
            device = led_devices.led_strip(pins = pin, topic = state_topic, set_topic = command_topic)
            return device

def mqtt_on_message(mqtt_topic, mqtt_message):
    global device
    message = mqtt_message.decode('utf-8')
    topic = mqtt_topic.decode('utf-8')
    print('recieved', topic, message)
    update_led_strip(loads(message))

def update_led_strip(message):
    global device
    global mqtt
    state = {}
    device.fade = False
    switch = None
    duration = None
    for key, value in message.items():
        if key in ('brightness', 'color', 'white_value'):
            state[key] = value
        if key == 'effect' and message['effect'] == 'fade':
            device.fade = True
        if key == 'transition':
            duration = value
        if key == 'state':
            switch = value
    if device.fade:
        device.update({'state':'ON'})
        if duration == None:
            duration = 300
        steps = duration *(1000/100)
        device._generate_incr(state, steps)
        init_state = device.dic_state
        # make a copy of the original state
        orig_state = {}
        for key, value in device.dic_state.items():
            if key in ('brightness', 'white_value'):
                orig_state[key] = value
            elif key == 'color':
                subdic = {}
                for subkey, subval in device.dic_state[key].items():
                    subdic[subkey] = subval
                orig_state[key] = subdic
        for s in range(steps):
            device._next_step(orig_state, s)
            if s % 10 == 0:
                mqtt.send_msg(device.topic, device.state)
                mqtt.check_msg()
                if not device.fade:
                    break
            time.sleep_ms(50)
    elif switch is not None: # update on or off
        state['state'] = switch
    device.update(state)
    mqtt.send_msg(device.topic, device.state)

def init_loop(config = None, mqtt = None, device = None):
    config = read_config()
    load_wifi(config)
    device = load_led_strip(config)
    mqtt   = load_mqtt(config, [device.set_topic])
    print(mqtt)
    return mqtt, device

def main_loop(mqtt, device):
    active = True
    mqtt.send_msg(device.topic, device.state)
    while active:
        mqtt.wait_msg()

if __name__ == '__main__':
    mqtt, device = init_loop()
    main_loop(mqtt, device)
