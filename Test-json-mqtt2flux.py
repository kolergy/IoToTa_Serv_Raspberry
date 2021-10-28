import random
import json

from paho.mqtt import client as mqtt_client
from influxdb  import InfluxDBClient

#hostMQTT  = '127.0.0.1'
hostMQTT  = 'localhost'
portMQTT  = 1883
topicMQTT = "python/mqtt" 
client_id = f'mqtt--json-flux-{random.randint(0, 100)}' # generate client ID with pub prefix randomly
usrMQTT   = 'pi'
pasMQTT   = 'PiMouche-01'

portFlux = 8086
hostFlux = 'localhost'

def connect_mqtt() -> mqtt_client:
    def on_connect(clientMQTT, userdata, flags, rc):
        if rc == 0:  print("Connected to MQTT Broker!")
        else:        print("Failed to connect, return code %d\n", rc)

    clientMQTT = mqtt_client.Client(client_id)
    clientMQTT.username_pw_set(usrMQTT, pasMQTT)
    clientMQTT.on_connect = on_connect
    clientMQTT.connect(hostMQTT, portMQTT)
    return clientMQTT


def subscribe(clientMQTT: mqtt_client, clientFlux):
    def on_message(clientMQTT, userdata, msg):
        new_message = msg.payload.decode()
        print(type(new_message))
        print(f"Received `{new_message}` from `{msg.topic}` topic")
        try:
            j = json.loads(new_message)
            print(j)
            for k in j:
                print("key: {}, value: {}".format(k, j[k]))
            #clientFlux.write_points(new_message)
        except ValueError as e:
            print("receved message is not a valid json. Error: {}".format(e))
    
    clientMQTT.subscribe(topicMQTT)
    clientMQTT.on_message = on_message


def run():
    clientMQTT = connect_mqtt()
    clientFlux = InfluxDBClient(host=hostFlux, port=portFlux)
    
    subscribe(clientMQTT, clientFlux)
    #clientFlux = InfluxDBClient(host='mydomain.com', port=8086, username='myuser', password='mypass' ssl=True, verify_ssl=True)
    #clientFlux.create_database('testMQTTpyFlux')
    ldb = clientFlux.get_list_database()
    print(ldb)
    clientFlux.switch_database('testMQTTpyFlux')

    clientMQTT.loop_forever()
    

if __name__ == '__main__':
    run()

