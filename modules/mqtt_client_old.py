from umqtt.simple import MQTTClient
from time import sleep


def basic_callback(topic, message):
    response = message.decode('utf-8')
    print(topic.decode('utf-8'), response)

def test_run():
    topics = ('home/hall/mirror', 'home/hall/mirror/set')
    ip = '192.168.1.10'
    host = 'test'
    client = mqtt_client(topics, host, ip)
    while True:
        client.check_msg()
        sleep(1)
    

class mqtt_client():
    def __init__(self, topics, client_id, mqtt_server_ip, callback = basic_callback, debug = False):
        self.server_ip =     mqtt_server_ip
        self.id =            client_id
        self.__mqtt_client = MQTTClient(self.id, self.server_ip)
        self.__callback =    callback
        self.topics =        list(topics)
        self.connected =     False
        self.debug =         debug
        self.__connect()

    def __str__(self):
        results = 'mqtt client\n  id      {}\n  server    {}\n  callback {}\n  topics  {}\n'
        return results.format(self.id, self.server_ip, self.__callback, self.topics)
        

    def __connect(self):
        if self.debug:
            print('id', self.id, 'ip' , self.server_ip)
        myclient = MQTTClient(self.id, self.server_ip)
        self.__mqtt_client = MQTTClient(self.id, self.server_ip)
        self.__mqtt_client.set_callback(self.__callback)
        self.__mqtt_client.connect()
        for tpc in self.topics:
            print('subscribing to topic ', tpc)
            self.__mqtt_client.subscribe(tpc)
        print('connected to mqtt server at {}'.format(self.server_ip))            
        self.connected = True


    def subscribe(self, topic):
        if topic not in self.topics:
            self.topics.append(topic)
            if self.connected:
                self.__mqtt_client.subscribe(topic)
    
    def unsubscribe(self, topic):
        if topic in self.topics:
            self.topics.pop(topic)
            # umqtt.simple does not implement an unsubscribe method    
        

    def check_msg(self):
        try:
            self.is_alive()
            if self.debug:
                print('checking for new messages')
            self.__mqtt_client.check_msg()
            self.connected = True
        except OSError:
            self.connected = False
            if self.debug:
                print('no connection to mqtt server')

    def send_msg(self, topic, message):
        tpc = topic.encode('utf-8')
        msg = message.encode('utf-8')
        self.__mqtt_client.publish(tpc,msg,1,True)
        print('published topic {}, message {}'.format(topic, message))  
        self.connected = True

    def is_alive(self):
    # check if connected is true and reconnect if it is not. if succesful, the 
    # function will return true, otherwise, false
        if not self.connected:
            self.__connect()
        return self.connected

