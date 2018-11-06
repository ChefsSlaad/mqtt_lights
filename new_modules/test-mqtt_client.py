import unittest
import os
from time import sleep_ms

import mqtt_client

def test_mqtt_connect(*args):
    pass

def test_callback(topic, message):
    global r_topic, r_message
    r_topic = topic.decode('utf-8')
    r_message = message.decode('utf-8')


class mqtt_broker():
    def __init__(self, port):
        os.popen('mosquitto -p {} > /dev/null 2>&1'.format(port))
    def kill(self):
        os.popen('pkill mosquitto > /dev/null 2>&1')

test_topics = ['test/test', 'test/test2']
send_id     = 'test_sender'
recv_id     = 'test_reviever'
null_server = '0.0.0.0'
real_server = '127.0.0.1'
mqtt_port   = 1899
r_topic     = None
r_message   = None


class mqtt_tests(unittest.TestCase):
    def setUp(self):
        self.broker = mqtt_broker(mqtt_port)
        self.sender = mqtt_client.mqtt_client(test_topics, send_id, real_server, mqtt_port, debug = True)
        self.reciev = mqtt_client.mqtt_client(test_topics, recv_id, real_server, mqtt_port, callback = test_callback, debug = True)

    def tearDown(self):
        self.sender.disconnect()
        self.reciev.disconnect()
        self.broker.kill()

    def test_init(self):
        self.sender.__connect = test_mqtt_connect
        test_client = self.sender

        self.assertEqual(test_client.id, send_id)
        self.assertEqual(test_client.server_ip, real_server)
        self.assertEqual(test_client.topics, test_topics)

    def test_real_init(self):
        test_client = self.sender
        self.assertEqual(test_client.id, send_id)
        self.assertEqual(test_client.server_ip, real_server)
        self.assertEqual(test_client.topics, test_topics)

    def test_mqtt_send(self):
        global r_topic, r_message

        s_topic = test_topics[0]
        s_message = 'hello world'
        self.sender.send_msg(s_topic, s_message)
        self.reciev.check_msg()
        self.assertEqual(s_topic, r_topic)
        self.assertEqual(s_message, r_message)

if __name__ == '__main__':
    unittest.main()
