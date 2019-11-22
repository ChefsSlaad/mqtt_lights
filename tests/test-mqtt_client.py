import unittest
import os
from time import time, sleep_ms, localtime
from urandom import getrandbits
from ujson import loads, dumps

import sys
sys.path.insert(1, '/home/marc/projects/mqtt_lights/new_modules')


import mqtt_client

import logger
test_topics = ['test/test', 'test/test2', 'mytest']
send_id     = 'test_sender'
recv_id     = 'test_reciever'
null_server = '0.0.0.0'
real_server = '127.0.0.1'
mqtt_port   = 1883
r_topic     = None
r_message   = None
debug_mqtt  = True

messages  = ['hello world', '1', 'ON', 'True', 'False', '1.090',
             '~!@#$%^&*()_+{}[]|\:;""<>?/']


def strftime():
    t = time()
    h = localtime()[3]
    m = localtime()[4]
    s = localtime()[5]
    return '{:2}:{:2}:{:2}'.format(h,m,s)


def getrandstr(size):
    letters = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*(){}\][;:"''",.?/`-=]12345678901'
    return ''.join(letters[getrandbits(6)] for _ in range(size))

def test_mqtt_connect(*args):
    pass

def silent_callback(topic, message):
    pass

def test_callback(topic, message):
    global r_topic, r_message
    r_topic = topic.decode('utf-8')
    r_message = message.decode('utf-8')

class mqtt_broker():
    def __init__(self, port = 1883, debug_mqtt = False ):
        self.port = port
        self.start()
    def start(self):
        os.popen('mosquitto > /dev/null 2>&1')
        if debug_mqtt: print('starting mosquitto server at port {} with pid {}'.format(self.port, os.popen('pgrep mosquitto')))
        sleep_ms(100)
    def kill(self):
        os.popen('pkill mosquitto > /dev/null 2>&1')
        sleep_ms(100)

class mqtt_tests(unittest.TestCase):
    def setUp(self):
        global r_topic, r_message
        r_topic = None
        r_message = None
        self.logger = logger.logger()
        self.broker = mqtt_broker(mqtt_port)
        self.sender = mqtt_client.mqtt_client(test_topics, send_id, real_server, mqtt_port, callback = None, debug = debug_mqtt, logger = self.logger)
        self.reciev = mqtt_client.mqtt_client(test_topics, recv_id, real_server, mqtt_port, callback = test_callback, debug = debug_mqtt, logger = self.logger)

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


    def test_mqtt_send_recieve(self):
        global r_topic, r_message
        for m in messages:
            for t in test_topics:
                self.sender.publish(t,m)
                self.reciev.wait_msg()
                self.assertEqual(t, r_topic)
                self.assertEqual(m, r_message)

    def test_use_check_msg(self):
        global r_topic, r_message
        global test_topics, messages
        recive_combos = list()
        topic_message_combos = list([(t,m) for t in test_topics for m in messages])
        for t, m in topic_message_combos:
            self.sender.publish(t,m)
        while len(recive_combos) != len(topic_message_combos):
            self.reciev.check_msg()
            recive_combos.append((r_topic,r_message))
        self.assertEqual(set(recive_combos), set(topic_message_combos))

    def test_send_unconnected(self):
    #what happens if we try to send multiple messages  with no connection
        global r_topic, r_message
        self.broker.kill()
        for m in messages:
            for t in test_topics:
                self.sender.publish(t,m)


    def test_recover_from_network_error(self):
        global r_topic, r_message
        for m in messages:
            for t in test_topics:
                self.broker.kill()
                self.sender.publish(t,m)
##                print(self.sender)
                self.broker.start()
                self.sender.publish(t,m)
                self.assertTrue(self.sender.connected)

    def test_load_stress_test(self):
        # send as many meaasages as possible in quick seccession
        global r_topic, r_message
        no = 1000
        for i in range(no):
            print(i, end = ' ')
            for t in test_topics:
                m = getrandstr(getrandbits(8))
                self.sender.publish(t,m)
                self.reciev.wait_msg()
                self.assertEqual(t, r_topic)
                self.assertEqual(m, r_message)

    def test_continuity(self):
        # send a contnuous load for xx hours
        global r_topic, r_message
        hrs = 8
        dur = 60*60*hrs
        start = time()
        i = 0
        while time()-start < dur:
            for t in test_topics:
                m = getrandstr(getrandbits(8))
                self.sender.publish(t,m)
                self.reciev.check_msg()
#                self.assertEqual(t, r_topic)
#                self.assertEqual(m, r_message)
                sleep_ms(200)
                print(strftime())
#                print('.', end ='')

if __name__ == '__main__':
    unittest.main()
