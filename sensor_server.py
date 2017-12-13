import time
import datetime

import paho.mqtt.client as mqtt



mqtt_server = '192.168.1.10'
client_name = 'listener'

micro_topic = 'home/woonkamer/boekenkast/sensor/microwave'
pir_topic   = 'home/woonkamer/boekenkast/sensor/pir'
logfile     = 'sensor.log'


client = mqtt.Client(client_name)
client.connect(mqtt_server)

client.subscribe(micro_topic)
client.subscribe(pir_topic)



def on_message(client, userdata, message):
    now = datetime.datetime.now().replace(microsecond=0)
    payload = str(message.payload.decode("utf-8"))
    topic = message.topic
    logstring = '{} sensor : {} value {} \n'.format(now, topic, payload)
    with open(logfile, 'a') as f:
        f.write(logstring)




client.on_message = on_message

client.loop_start()

while True:
    time.sleep(1)

