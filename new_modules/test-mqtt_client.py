import unittest
import os
from time import sleep_ms
from ujson import loads, dumps
import mqtt_client

test_topics = ['test/test', 'test/test2']
send_id     = 'test_sender'
recv_id     = 'test_reciever'
null_server = '0.0.0.0'
real_server = '127.0.0.1'
mqtt_port   = 1899
r_topic     = None
r_message   = None
debug_mqtt  = True

messages  = ['hello world', '1', 'ON', 'True', 'False', '1.090',
             '~!@#$%^&*()_+{}[]|\:;""<>?/']

def test_mqtt_connect(*args):
    pass

def silent_callback(topic, message):
    pass

def test_callback(topic, message):
    global r_topic, r_message
    r_topic = topic.decode('utf-8')
    r_message = message.decode('utf-8')

class mqtt_broker():
    def __init__(self, port):
        self.port = port
        self.start()
    def start(self):
        os.popen('mosquitto -p {} > /dev/null 2>&1'.format(self.port))
        print('starting mosquitto server at port {} with pid {}'.format(self.port, os.popen('pgrep mosquitto')))
    def kill(self):
        os.popen('pkill mosquitto > /dev/null 2>&1')

class mqtt_tests(unittest.TestCase):
    def setUp(self):
        global r_topic, r_message
        r_topic = None
        r_message = None
        self.broker = mqtt_broker(mqtt_port)
        self.sender = mqtt_client.mqtt_client(test_topics, send_id, real_server, mqtt_port, callback = silent_callback, debug = debug_mqtt)
        self.reciev = mqtt_client.mqtt_client(test_topics, recv_id, real_server, mqtt_port, callback = test_callback, debug = debug_mqtt)

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
        self.assertTrue(test_client.connected)
    def test_mqtt_send_recieve(self):
        global r_topic, r_message

        for m in messages:
            for t in test_topics:
                self.sender.send_msg(t,m)
                self.reciev.wait_msg()
                self.assertEqual(t, r_topic)
                self.assertEqual(m, r_message)

    def test_recover_from_network_error(self):
        global r_topic, r_message
        for m in messages:
            for t in test_topics:
                self.broker.kill()
                self.sender.send_msg(t,m)
                print(self.sender)
                self.assertFalse(self.sender.connected)
                self.broker.start()



if __name__ == '__main__':
    unittest.main()
