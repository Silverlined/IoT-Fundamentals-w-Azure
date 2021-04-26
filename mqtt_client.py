#!/usr/bin/env python3
import time
import paho.mqtt.client as paho
import ssl
import uuid
import json
from datetime import datetime
from influxdb import InfluxDBClient

BROKER_IP = "127.0.0.1"
db_client = None
topic = "bme280"


def message_callback(client, userdata, message):
    decoded_msg = str(message.payload.decode("utf-8"))
    values = decoded_msg.split(",")
    print(values)
    json_data = [
        {
            "measurement": "sensorEvents",
            "tags": {"sensor": "BME280"},
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {"temperature": float(values[0]), "humidity": float(values[1]), "pressure": float(values[2])},
        }
    ]
    if db_client:
        print(db_client.write_points(json_data))


def main():
    global db_client
    db_client = InfluxDBClient(host="localhost", port=8086, database="home")
    client = paho.Client(str(uuid.uuid1()))
    client.tls_set(
        "./ssl/ca.crt",
        "./ssl/client.crt",
        "./ssl/client.key",
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS,
    )

    client.on_message = message_callback
    #####
    print("Connecting to broker ", BROKER_IP)
    client.connect(BROKER_IP, 8883, 60)  # connect
    print("Subscribing to topic ", topic)
    client.subscribe(topic)  # subscribe
    client.loop_forever()  # start loop to process received messages


if __name__ == "__main__":
    main()

