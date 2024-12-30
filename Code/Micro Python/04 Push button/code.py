"""
* Firmware:
 - Micropython 1.24.1
* Hardware:
 - Raspberry Pi Pico v1
 - Push switch (note inverse polarity)
     Pin1 (GND 		=> 3v3)
     Pin2 (VCC		=> GND)
     Pin3 (S		=> GP0)
* Description:
 Displays 1 if the button is pressed, 0 if it isn't (updated every .5s)
"""     

import machine
import random
import time

# Set up button
btn = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    print(btn.value())
    time.sleep(1)
    
    