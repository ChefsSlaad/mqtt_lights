import unittest
import os
from time import time, sleep_ms, localtime
from urandom import getrandbits
from ujson import loads, dumps
from umqtt.simple import MQTTClient

import sys
sys.path.insert(1, '/home/marc/projects/mqtt_lights/new_modules')


import logger

recv_id     = 'test_reciever'
port        = 1883
r_topic     = None
r_message   = None
server      = "127.0.0.1"
log_topic   = "logger"

messages  = ['hello world', '1', 'ON', 'True', 'False', '1.090',
             '~!@#$%^&*()_+{}[]|\:;""<>?/']

mqtt_conf1 = { "server_adress": server,
               "topic":         log_topic,
               "client_id":     "logger",
               "active":        True
             }

def strftime():
    t = time()
    h = localtime()[3]
    m = localtime()[4]
    s = localtime()[5]
    return '{:2}:{:2}:{:2}'.format(h,m,s)

def getrandstr(size):
    letters = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*(){}\][;:"''",.?/`-=]12345678901'
    return ''.join(letters[getrandbits(6)] for _ in range(size))

def return_topic_and_message(topic, message):
    global r_topic, r_message
    r_message = message.decode('utf-8')
    r_topic = topic.decode('utf-8')
    return r_topic, r_message

class mqtt_broker():
    def __init__(self, port = 1883):
        self.port = port
        self.start()
    def start(self):
        os.popen('mosquitto > /dev/null 2>&1')
        sleep_ms(100)
    def kill(self):
        os.popen('pkill mosquitto > /dev/null 2>&1')
        sleep_ms(100)

class logger_tests(unittest.TestCase):
    def setUp(self):
        global r_message
        self.broker = mqtt_broker()
        self.reciever = MQTTClient("test_reciever", server )
        self.reciever.set_callback(return_topic_and_message)
        self.reciever.connect()
        self.reciever.subscribe(log_topic)
        self.logger = logger.logger(mqtt_conf1)

    def tearDown(self):
        global r_message
        r_message = None
        self.logger.close()
        self.reciever.disconnect()
#        self.broker.kill()


    def test_init(self):
        self.assertEqual(self.logger.active, True)
        self.assertEqual(self.logger.buffer, [])
        self.assertEqual(self.logger.topic, mqtt_conf1['topic'].encode('utf-8'))

    def test_log(self):
        global r_message, r_topic
        for msg in messages:
            self.logger.log(msg)
            self.reciever.wait_msg()
            self.assertIn(msg, r_message)


    def test_deactivate_reactivate(self):
        global r_message
        msg = "testing_activation"
        # part the first - check if logger is active
        self.assertEqual(self.logger.activate(), True, 'logger not active')
        #deactivate logger and check that no message is sent
        self.logger.activate(False)
        self.logger.log(msg)
        self.reciever.check_msg()
        self.assertEqual(self.logger.activate(), False, 'logger has not been deactivated')
        self.assertEqual(r_message, None, 'message r_message is not none but {}'.format(r_message))
        #reactivate and check that message is recieved now
        self.logger.activate(True)
        self.logger.log(msg)
        self.reciever.wait_msg()
        self.assertIn(msg, r_message, "message {} is not in {}".format(msg, r_message))

    def test_log_buffering(self):
        ''' test if multiple random strings logged end up the same
        '''
        global r_message
        for i in range(5):
            self.logger.buffer.append(getrandstr(25))
        msg = '\n'.join(self.logger.buffer.copy())
        self.logger.writelog()
        self.reciever.wait_msg()
        self.assertIn(msg, r_message, "message {} is not in {}".format(msg, r_message))




    def test_multiple_buffers(self):
        ''' test if multiple random strings logged end up the same
        '''
        global r_message
        for i in range(5):
            for j in range(5):
                self.logger.buffer.append(getrandstr(25))
            msg = '\n'.join(self.logger.buffer.copy())
            self.logger.writelog()
            self.assertEqual(self.logger.buffer, [], "buffer is not empty")
            self.reciever.wait_msg()
            self.assertIn(msg, r_message, "message {} is not in {}".format(msg, r_message))

    def test_close_clean(self):
        global r_message
        self.logger.log(getrandstr(25))
        self.reciever.wait_msg() # dont care about the message
        self.logger.close()
        self.assertEqual(self.logger.buffer, [], "buffer is not empty")

    def test_close_with_buffer(self):
        global r_message
        msg = getrandstr(25)
        self.logger.buffer.append(msg)
        self.logger.close()
        self.reciever.wait_msg() # dont care about the message
        self.assertEqual(self.logger.buffer, [], "buffer is not empty")
        self.assertIn(msg, r_message, "message {} is not in {}".format(msg, r_message))

if __name__ == '__main__':
    unittest.main()
