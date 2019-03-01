from umqtt.simple import MQTTClient
from time import sleep_ms, time

def basic_callback(topic, message):
    response = message.decode('utf-8')
    print(topic.decode('utf-8'), response)

class mqtt_client():
    def __init__(self, topics, client_id, mqtt_server_ip, port = 1883, callback = basic_callback, debug = False):
        self.server_ip =     mqtt_server_ip
        self.port =          port
        self.id =            client_id
        self.__mqtt_client = MQTTClient(self.id, self.server_ip)
        self.__callback =    callback
        self.topics =        list(topics)
        self.connected =     False
        if debug:
            from logger import logger
            self.logger =    logger()
        else:
            from logger import dummy_logger
            self.logger =    dummy_logger()
        self.__last_reset =  time()
        self.__reset_time =  1800 # 30 minutes
        self.__connect()

    def __str__(self):
        results = 'mqtt client\n  id        {}\n  server    {}\n  connected {}\n  callback  {}\n  topics    {}\n'
        return results.format(self.id, self.server_ip, self.connected, self.__callback, self.topics)

    def __connect(self):
        try:
            self.logger.log('connecting to mqtt', 'id:', self.id, 'ip:', self.server_ip)
            self.__mqtt_client = MQTTClient(self.id, self.server_ip, self.port)
            self.__mqtt_client.connect()
            if self.__callback != None:
                self.__mqtt_client.set_callback(self.__callback)
                for tpc in self.topics:
                    self.logger.log(self.id, 'subscribing to topic ', tpc)
                    self.__mqtt_client.subscribe(tpc)
            self.logger.log(self.id, 'connected to mqtt server at {}'.format(self.server_ip))
            self.__last_reset = time()
            self.connected = True
        except OSError as err:
            print(self.id, 'unable to connect to mqtt server \n', err)
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
            # reset connection every xx minutes
            if time() - self.__last_reset > self.__reset_time:
                self.reconnect()
            self.logger.log(self.id, 'checking for new messages')
            if blocking:
                self.__mqtt_client.wait_msg()
            else:
                self.__mqtt_client.check_msg()
            self.connected = True
        except OSError as err:
            self.connected = False
            self.logger.log(self.id, 'no connection to mqtt server \n', err)

    def publish(self, topic, message):
        tpc = topic.encode('utf-8')
        msg = message.encode('utf-8')
        try:
            self.is_alive()
            self.__mqtt_client.publish(tpc,msg,0,True)
            self.logger.log(self.id, 'published topic {}, message {}'.format(topic, message))
            self.connected = True
        except OSError as err:
            self.logger.log(self.id, 'error publishing topic {}, message {}. \n not connected to mqtt server\n'.format(topic, message), err)
            self.connected = False

    def reconnect(self):
        self.logger.log(self.id, 'reconnecting now')
        self.__mqtt_client.disconnect()
        sleep_ms(1000)
        self.__connect()

    def disconnect(self):
        self.logger.log(self.id, 'disconnecting now')
        try:
            self.__mqtt_client.disconnect()
        except OSError as err:
            self.connected = False
            self.logger.log(self.id, 'no connection to mqtt server \n', err)

    def is_alive(self):
    # check if connected is true and reconnect if it is not. if succesful, the
    # function will return true, otherwise, false
        if not self.connected:
            self.logger.log('disconnected, attempting reconnect')
            self.__connect()
        return self.connected
