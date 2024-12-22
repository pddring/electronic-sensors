"""
Firmware:
- Micropython 1.24.1
Hardware:
- Raspberry Pi Pico v1
- DHT11 temperature and humidity sensor
    Pin 1 (S)	=> GP0
    Pin 2 (VDD)	=> 3.3v
    Pin 3 (GND) => GND
Description:
- Reads temperature ('C) and humidity (%) each second
"""
import machine
import dht
import time
sensor = dht.DHT11(machine.Pin(0))

while True:
    sensor.measure()
    temp = sensor.temperature()
    humidity = sensor.humidity()
    print("Temperature: {}'C Humidity: {}%".format(temp, humidity))
    time.sleep(1)