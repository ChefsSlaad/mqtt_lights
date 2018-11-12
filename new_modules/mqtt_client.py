from umqtt.simple import MQTTClient
from time import sleep


def basic_callback(topic, message):
    response = message.decode('utf-8')
    print(topic.decode('utf-8'), response)

def test_run():
    topics = ('home/hall/mirror', 'home/hall/mirror/set')
    ip = '10.0.0.10'
    host = 'test'
    client = mqtt_client(topics, host, ip)
    while True:
        client.check_msg()
        sleep(1)

class mqtt_client():
    def __init__(self, topics, client_id, mqtt_server_ip, port = 1883, callback = basic_callback, debug = False):
        self.server_ip =     mqtt_server_ip
        self.port =          port
        self.id =            client_id
        self.__mqtt_client = MQTTClient(self.id, self.server_ip)
        self.__callback =    callback
        self.topics =        list(topics)
        self.connected =     False
        self.debug =         debug
        self.__connect()

    def __str__(self):
        results = 'mqtt client\n  id        {}\n  server    {}\n  connected {}\n  callback  {}\n  topics    {}\n'
        return results.format(self.id, self.server_ip, self.connected, self.__callback, self.topics)


    def __connect(self):
        try:
            if self.debug:
                print('id', self.id, 'ip' , self.server_ip)
            myclient = MQTTClient(self.id, self.server_ip, self.port)
            self.__mqtt_client = MQTTClient(self.id, self.server_ip)
            self.__mqtt_client.set_callback(self.__callback)
            self.__mqtt_client.connect()
            for tpc in self.topics:
                if self.debug: print(self.id, 'subscribing to topic ', tpc)
                self.__mqtt_client.subscribe(tpc)
            if self.debug: print(self.id, 'connected to mqtt server at {}'.format(self.server_ip))
            self.connected = True
        except OSError:
            if self.debug: print(self.id, 'unable to connect to mqtt server')
            self.connected = False

    def subscribe(self, topic):
        if topic not in self.topics:
            self.topics.append(topic)
            if self.connected:
                self.__mqtt_client.subscribe(topic)

    def unsubscribe(self, topic):
        if topic in self.topics:
            self.topics.pop(topic)
            # umqtt.simple does not implement an unsubscribe method

    def wait_msg(self):
        self.check_msg(blocking = True)

    def check_msg(self, blocking = False):
        try:
            self.is_alive()
            if self.debug: print(self.id, 'checking for new messages')
            if blocking:
                self.__mqtt_client.wait_msg()
            else:
                self.__mqtt_client.check_msg()
            self.connected = True
        except OSError:
            self.connected = False
            if self.debug: print(self.id, 'no connection to mqtt server')

    def send_msg(self, topic, message):
        tpc = topic.encode('utf-8')
        msg = message.encode('utf-8')
        try:
            self.is_alive()
            self.__mqtt_client.publish(tpc,msg,0,True)
            if self.debug: print(self.id, 'published topic {}, message {}'.format(topic, message))
            self.connected = True
        except OSError:
            if self.debug: print(self.id, 'error publishing topic {}, message {}. \n not connected to mqtt server'.format(topic, message))
            self.connected = False

    def reconnect(self):
        if self.debug: print(self.id, 'reconnecting now')
        self.__mqtt_client.disconnect()
        sleep(1)
        self.__connect()

    def disconnect(self):
        if self.debug: print(self.id, 'disconnecting now')
        self.__mqtt_client.disconnect()

    def is_alive(self):
    # check if connected is true and reconnect if it is not. if succesful, the
    # function will return true, otherwise, false
        if not self.connected:
            if self.debug: print('disconnected, attempting reconnect')
            self.__connect()
        return self.connected
