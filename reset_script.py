import time
import datetime

import paho.mqtt.client as mqtt



mqtt_server = '192.168.1.10'
client_name = 'listener'

boekenkast  = "home/controller/woonkamer/boekenkast"
light1_set   = "home/woonkamer/boekenkast/light/light1/set"
client = mqtt.Client(client_name)
client.connect(mqtt_server)

print('sending reset signal to', boekenkast)
client.publish(boekenkast, "RESET")

