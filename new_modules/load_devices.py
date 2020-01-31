import gc

def read_config(config_file = None):
    from os import stat, listdir
    from ujson import load
    if config_file == None: #if no file is not specified, read the first config file in the root dir
        config_file = [f for f in sorted(listdir()) if f[-5:] == '.json'][0]
    try:
        if stat(config_file)[6] != 0:
            print('reading file', config_file)
            with open(config_file) as read_file:
                config = load(read_file)
    except OSError:
        print('cannot read', config_file)
        config = None
    print("file {} loaded succesfully".format(config_file))
    return config

def load_wifi(config):
    import wifi_config
    gc.collect()
    if 'network' in config:
        networks = config['network']
        wifi_config.scan_and_connect(networks)

def load_mqtt(config, topics, callback):
    gc.collect()
    import mqtt_client
    # create a list of all the topics to subscribe to (aka command topics)
    name = config.get('name', 'default_client')
    mqtt_config = config.get('mqtt_server', {'server_adress':'0.0.0.0'})
    print(mqtt_config)
    debug = mqtt_config.get('debug', False)
    mqtt = mqtt_client.mqtt_client(topics = topics, client_id = name, mqtt_server_ip= mqtt_config['server_adress'], callback = callback, debug=debug)
    return mqtt

def load_devices(configuration):
    devices = []
    topics = []
    for id, conf in configuration.items():
        gc.collect()
        if isinstance(conf, dict) and "type" in conf.keys():
            if conf["type"] == "led":
                from led_pwm import led_pwm
                devices.append(led_pwm(conf))
                topics.append(conf["command_topic"])
            elif conf["type"] == "led_strip":
                from led_devices import led_strip
                devices.append(led_strip(conf))
                topics.append(conf["command_topic"])
            elif conf["type"] == "binary_sensor":
                from binary_sensor import binary_sensor
                devices.append(binary_sensor(conf))
            elif conf["type"] == "temp_sensor":
                from temp_sensor import temp_sensor
                devices.append(temp_sensor(conf))
            print("found a {} \n   {}".format(conf["type"], devices[-1]))
    return devices, topics
