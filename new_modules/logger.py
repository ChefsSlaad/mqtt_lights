from time import time
from umqtt.simple import MQTTClient

mqtt_conf = { "server_adress": "10.0.0.10",
                      "topic": "logger",
                      "client_id": "logger"
                    }

def print_time(the_time):
    secs, ms = divmod(the_time, 1)
    mins, sec = divmod(secs, 60)
    hrs, min = divmod(mins, 60)
    return '{:0>3}:{:0>2}:{:0>2}.{:0<3}'.format(int(hrs) % 1000, int(min), int(sec), round(ms*1000))

class dummy_logger():
    def activate(self, *args):
        pass
    def log(self, *args):
        pass

class logger():
    def __init__(self, mqtt_config = mqtt_conf, active = True):
        self.start_time = time()
        self.active    = active
        self.buffer = []
        self.mqtt_client = None
        self.topic = mqtt_config["topic"].encode("utf-8")
        self.activate(active)
        self.configure_mqtt(mqtt_config)


    def __exit__(self):
        self.close()

    def __del__(self):
        self.close()

    def writelog(self):
        msg = "\n".join(self.buffer).encode("utf-8")
#        print(msg)
        self.mqtt_client.connect()
        self.mqtt_client.publish(self.topic, msg)
        self.buffer = []

    def activate(self, active = None):
        if active == None:
            return self.active
        else:
            self.active = active
        return self.active

    def configure_mqtt(self, mqtt_config):
        self.mqtt_client = MQTTClient(mqtt_config["client_id"], mqtt_config["server_adress"])
        self.mqtt_client.connect()

    def log(self, *logstrings):
# logs to a file with format hh:mm:ss:mss    log message
        if self.active:
            the_time = time()
            msg = str(print_time(the_time)) + '  ' + ' '.join(logstrings)
            self.buffer.append(msg)
            self.writelog()

    def close(self):
        self.writelog()
        self.mqtt_client.disconnect()


def test():
    mqtt_conf = {"server_adress": "127.0.0.1",
                 "topic": "logger",
                 "client_id": "test"
                 }
    log = logger(mqtt_conf)
    log.log('hello', 'world')

r_message = None
def print_tpc_and_msg(tpc, msg):
    global r_topic
    global r_message
    r_topic = tpc.decode("utf-8")
    r_message = msg.decode("utf-8")



if __name__ == "__main__":
    client = MQTTClient("reciever", "127.0.0.1")
    client.set_callback(print_tpc_and_msg)
    client.connect()
    client.subscribe("logger")
    mqtt_conf = {"server_adress": "127.0.0.1",
                 "topic": "logger",
                 "client_id": "test"
                 }
    log = logger(mqtt_conf)
    log.log('hello', 'world')
    client.wait_msg()
    print(r_message)
    r_message = None
    print(log.activate())
    log.activate(False)
    log.log("test2")
    client.check_msg()
    print(r_message)
