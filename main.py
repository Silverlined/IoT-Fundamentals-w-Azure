from machine import Pin, I2C,reset
from utime import sleep_ms, time
from bme280_driver import BME280
from umqttsimple import MQTTClient
from config import mqtt, tls
import gc
gc.collect()

# Default I2C pins 18 (SCL) and 19 (SDA)
i2c = I2C(0)

def connect_MQTT():
    ssl_params = {}
    client = MQTTClient(mqtt["CLIENT_ID"], mqtt["BROKER_IP"], port=8883, ssl=True, ssl_params=tls)
    response = client.connect()
    print("Connected to %s MQTT broker" % mqtt["BROKER_IP"])
    return client

def restart_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep_ms(5000)
    reset()
  
def publish_BME280(sensor, client):
    temperature = sensor.temperature
    humidity = sensor.humidity
    pressure = sensor.pressure
    print("Values: %s, %s, %s" % (temperature, humidity, pressure))
    
    msg = b'%s, %s, %s' % (temperature, humidity, pressure)
    client.publish(mqtt["PUB_TOPIC"], msg)
  
def main():
    counter = 0
    last_time = 0
    interval = 5
    
    try:
        client = connect_MQTT()
    except OSError as e:
        restart_reconnect()
  
    while True:
        bme = BME280(i2c=i2c)
        try:
            client.check_msg()
            if (time() - last_time) > interval:
                publish_BME280(bme, client)
                last_time = time()
                counter += 1
        except OSError as e:
            restart_reconnect()
        sleep_ms(200)

        
if __name__ == "__main__":
    main()
