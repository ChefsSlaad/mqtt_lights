import time
from ujson import loads, dumps

config  = None
mqtt    = None
device  = None
led     = None
debug   = False

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
    mqtt = mqtt_client.mqtt_client(topics, name, mqtt_config['server_adress'], callback = mqtt_on_message, debug=debug)
    return mqtt

def load_onboard_led():
    import led_devices
    onboard_led = led_devices.led_pwm(2,inverted = True)
    return onboard_led

def load_led_strip(config):
    import led_devices
    for i in config:
        item = config[i]
        if "type" in item and item["type"] == "led_strip":
            state_topic   = item["state_topic"]
            command_topic = item["command_topic"]
            pin           = item["pin"]
            device = led_devices.led_strip(pins = pin, topic = state_topic, set_topic = command_topic)
            return device

def mqtt_on_message(mqtt_topic, mqtt_message):
    global device
    global led
    led.on()
    message = mqtt_message.decode('utf-8')
    topic = mqtt_topic.decode('utf-8')
    print('recieved', topic, message)
    state = loads(message)
    if 'effect' in state.keys():
        handle_transition(state, device, mqtt)
    else:
        device.stop_transition()
        device.update(state)
    led.off()

def handle_transition(state, device, mqtt):
    ms_wait = 100
    steps_per_second = 1000/ms_wait
    steps = 3000 # (5 min)
    if 'transition' in state.keys():
        steps = state['transition'] * steps_per_second
    effect = state['effect']
    device.init_effect(state, effect, steps)
    for step in range(steps):
        time.sleep_ms(ms_wait)
        device.next_step()
        if step % steps_per_second == 0: # once per second
            mqtt.check_msg()
            mqtt.publish(device.topic, device.state)

def init_loop(config = None, mqtt = None, device = None):
    config = read_config()
#    load_wifi(config)
    device = load_led_strip(config)
    mqtt   = load_mqtt(config, [device.set_topic])
    led    = load_onboard_led()
    print(mqtt)
    return mqtt, device, led

def main_loop(mqtt, device, led):
    active = True
    while active:
        mqtt.publish(device.topic, device.state)
        mqtt.wait_msg()

##qblink after message

if __name__ == '__main__':
    mqtt, device, led = init_loop()
    main_loop(mqtt, device, led)
