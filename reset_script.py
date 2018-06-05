import time
import datetime

import paho.mqtt.client as mqtt



mqtt_server = '192.168.1.10'
client_name = 'listener'

boekenkast  = "home/controller/woonkamer/boekenkast"
servieskast  = "home/controller/woonkamer/servieskast"
schemerlamp  = "home/controller/woonkamer/bank_schemerlamp"
gordijn_lang  = "home/controller/woonkamer/gordijn_lang"

client = mqtt.Client(client_name)
client.connect(mqtt_server)

print('sending reset signal to', boekenkast)
client.publish(boekenkast, "RESET")
client.publish(servieskast, "RESET")
client.publish(schemerlamp, "RESET")
client.publish(gordijn_lang, "RESET")

