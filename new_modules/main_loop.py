from time import sleep_ms
from json import loads, dumps

import load_devices

mqtt    = None
devices = None

def init():
    config = load_devices.read_config()
    devices, topics = load_devices.load_devices(config)
    load_devices.load_wifi(config)
    mqtt = load_devices.load_mqtt(config, topics, callback = mqtt_on_message)
    return config, mqtt, devices

def mqtt_on_message(mqtt_topic, mqtt_message):
    global devices
    topic = mqtt_topic.decode('utf-8')
    message = mqtt_message.decode('utf-8')
    for dev in devices:
        if dev.set_topic == topic:
            dev.update(message)
            mqtt.publish(dev.topic, dev.state)

def devices_check_state(devices, mqtt):
    for dev in devices:
        print(dev)
        dev.check_state()
        if dev.old_state != dev.state:
            mqtt.publish(dev.topic, dev.state)

def main_loop(devices, mqtt):
    while True:
        devices_check_state(devices, mqtt)
        mqtt.check_msg()
        sleep_ms(500)

def run_main_loop():
    global mqtt, devices
    config, mqtt, devices = init()
    main_loop(devices, mqtt)

if __name__ == '__main__':
    run_main_loop()
