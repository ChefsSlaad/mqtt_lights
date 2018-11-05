import unittest
import os

import mqtt_client

def test_mqtt_connect(*args):
    pass

def test_mqtt_send(topic, message):
    pass

def test_mqtt_check_message(*args):
    #call the callback function here
    pass

class mqtt_broker():
    def __init__(self, port):
        self.__process = os.popen('mosquitto -p {}'.format(port))
    def kill():
        self.__process.close()
        os.popen('pkill mosquitto')

test_topics = ['test/test', 'test/test2']
id = 'tester'
mqtt_server = '0.0.0.0'


class mqtt_tests(unittest.TestCase):

    def test_init(self):
        test_client = mqtt_client.mqtt_client(test_topics, id, mqtt_server)
        mqtt_client.__connect = test_mqtt_connect
        mqtt_client.send_msg = test_mqtt_send
        mqtt_client.check_msg = test_mqtt_check_message

        self.assertEqual(test_client.id, id)
        self.assertEqual(test_client.server_ip, mqtt_server)
        self.assertEqual(test_client.topics, test_topics)

    def test_single_send(self):
        broker = mqtt_broker(1899)
        test_client = mqtt_client.mqtt_client(test_topics, id, mqtt_server)


if __name__ == '__main__':
    unittest.main()
