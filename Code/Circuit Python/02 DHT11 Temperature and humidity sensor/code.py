"""
Adventures in Electronics
* Firmware:
 - CircuitPython v9.2.1
* Hardware:
 - Raspberry pi pico in pico explorer board
 - DHT11 temperature and humidity sensor
     Pin1 (S 	=> GP0)
     Pin2 (VDD	=> 3v3)
     Pin3 (GND	=> GND)
* Description:
 Reads temperature ('C) and humidity (%) every second and
 displays readings on screen
"""
import picoexplorer
import adafruit_dht
import board
import time

dhtDevice = adafruit_dht.DHT11(board.GP0)
picoexplorer.init()
while True:
    # read temperature
    temperature_c = dhtDevice.temperature
    
    t = "Temp: {:.1f} C".format(temperature_c)
    picoexplorer.set_line(3, t)
    
    # read humidity
    humidity = dhtDevice.humidity
    h = "Humidity: {}% ".format(humidity)
    picoexplorer.set_line(4, h)
    
    # display both values to console
    print(t,h)

    # shouldn't read values more than 1Hz
    time.sleep(1.0)