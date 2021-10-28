# IoTOtA_Serv_Raspberry
Server side for IoTOtA on a Raspberry Pi (simple MQTT + InfluxDb + Graphana

Work In Progress!  It is not yet working!!!

test with an other terminal on the Pi
mosquitto_pub -d -t python/mqtt -m "{ \"measurement\": \"temperatures\", \"time\": \"2021-10-22 17:50:00\", \"fields\": { \"temp01\": 19.5}, \"tags\": {}}"
