import time

config  = None
devices = []
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
            if dev.set_topic != None:
                all_topics.append(dev.set_topic)
        except AttributeError:
            print('no topic found for', dev.type)
    name = config['name']
    mqtt_config = config['mqtt_server']
    mqtt = mqtt_client.mqtt_client(all_topics, name, mqtt_config['server_adress'], callback = mqtt_on_message, debug=True)
    return mqtt

def load_switch(config, devices):
    from switches import switch
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "switch":
            state_topic = item["state_topic"]
            command_topic = item["command_topic"]
            pin           = item["pin"] 
            invert        = not item["high_on"]
            device = switch(pin = pin, topic = state_topic, set_topic = command_topic, inverted = invert)
            devices.append(device)
    return devices
    
def load_led(config, devices):
    from led_devices import led_pwm
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "led":
            state_topic = item["state_topic"]
            command_topic = item["command_topic"]
            pin           = item["pin"] 
            invert        = not item["high_on"]
            device = led_pwm(pin = pin, topic = state_topic, set_topic = command_topic, inverted = invert)
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
            device = led_devices.led_strip(pins = pin, topic = state_topic, set_topic = command_topic)
            devices.append(device)
    return devices

def load_button(config, devices):
    import button
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "button":
            state_topic = item["state_topic"]
            pin           = item["pin"] 
            invert        = not item["high_on"]
            device = button.button(pin = pin, topic = state_topic, inverted = invert)
            devices.append(device)
    return devices

def load_sensor(config, devices):
    import binary_sensor
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "binary_sensor":
            state_topic = item["state_topic"]
            pin         = item["pin"] 
            device = binary_sensor.binary_sensor(pin = pin, topic = state_topic)
            devices.append(device)
    return devices

def mqtt_on_message(mqtt_topic, mqtt_message):
    message = mqtt_message.decode('utf-8')
    topic = mqtt_topic.decode('utf-8')
    print('recieved', topic, message)
    global devices
    for device in devices:
        if device.set_topic == topic:
            if device.type in valid_set_devices:
                device.update(message)
    print('finished mqtt_on_message')

def load_all(config, devices):
    config = read_config()
    load_wifi(config)
    gc.collect()
    print('loading switch, free memory {}'.format(gc.mem_free()))
    load_switch(config, devices)
    gc.collect()
    print('loading button, free memory {}'.format(gc.mem_free()))
    load_button(config, devices)
    gc.collect()
    print('loading sensor, free memory {}'.format(gc.mem_free()))
    load_sensor(config, devices)
    gc.collect()
    print('loading led, free memory {}'.format(gc.mem_free()))
    load_led(config, devices)
    gc.collect()
    print('loading led_strip, free memory {}'.format(gc.mem_free()))
    load_led_strip(config, devices)
    gc.collect()
    print('loading mqtt, free memory {}'.format(gc.mem_free()))
    mqtt = load_mqtt(config, devices)
    gc.collect()
    print('free memory {}'.format(gc.mem_free()))
    return config, devices, mqtt

def check_for_changes_and_update(devices, mqtt):
    for device in devices:
        if device.type == 'led_strip':
            print('current', device.state, end = ' ')
            print('old_sta', device.old_state)
        if device.state != device.old_state:
            topic = device.topic
            state = device.state
            mqtt.send_msg(topic, state)
            device.old_state = device.state
        if device.type in valid_input_devices:
            device.check_state()
    mqtt.check_msg() 

def init_loop(config, devices):
    config, mydevices, mqtt = load_all(config, devices)
    for dev in mydevices:
        print(dev)
    print(mqtt)
    return mqtt, mydevices


def main_loop(mqtt, devices, reconnect_interval):
    active = True
    reconnect_time = time.time() + reconnect_interval
    while active:
        time.sleep_ms(500)
        check_for_changes_and_update(devices, mqtt)
        print('free memory {}'.format(gc.mem_free()), end = ' ')
        if reconnect_time < time.time() :
            mqtt.reconnect()
            reconnect_time = time.time() + reconnect_interval


if __name__ == '__main__':
    reconnect_interval = 3600
    mqtt, mydevices = init_loop(config, devices)
    mqtt.check_msg()
    time.sleep_ms(1000)
    main_loop(mqtt, mydevices, reconnect_interval)

