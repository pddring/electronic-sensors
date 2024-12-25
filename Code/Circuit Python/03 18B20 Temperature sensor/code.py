"""
Adventures in Electronics
* Firmware:
 - CircuitPython v9.2.1
* Hardware:
 - Raspberry pi pico in pico explorer board
 - 18B20 temperature sensor
     Pin1 (GND/G	=> GND)
     Pin2 (VDD/R	=> 3v3)
     Pin3 (DQ/Y		=> GP0)
     
* Description:
 Reads temperature ('C) every second and displays on screen
 Spins motor 1 if temperature is less than 16.
* Buttons:
 A: auto mode (spins if temperature is less than 16)
 B: manual mode (use X and Y to change speed)
 X: increase speed by .1 in manual mode
 Y: decrease speed by .1 in manual mode
"""
import picoexplorer
import board
import time
import adafruit_ds18x20
from adafruit_onewire.bus import OneWireBus
ow_bus = OneWireBus(board.GP0)
mode = "auto"
speed = 0.0
# scan for all sensors (you can have lots connected to the same pin)
devices = ow_bus.scan()

if len(devices) == 0:
    print("No devices found")
else:
    id = "".join([hex(i)[2:] for i in devices[0].rom])
    print("ROM = {} \tFamily = 0x{:02x}".format(id, devices[0].family_code))

    picoexplorer.init()

    # only connect to the first device found
    ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])

    while True:
        # read temperature
        temperature_c = ds18b20.temperature
        t = 'Temp: {0:0.3f} °C'.format(temperature_c)
        print(t)
        picoexplorer.set_line(3, t)
        
        # switch on the motor if temperature is below 16'
        if mode == "auto":
            if temperature_c < 16:
                speed = .3
            else:
                speed = 0
        if mode == "manual":
            if not picoexplorer.buttons["X"].value:
                speed += 0.1
            if not picoexplorer.buttons["Y"].value:
                    speed -= 0.1
        if not picoexplorer.buttons["A"].value:
            mode = "auto"
        if not picoexplorer.buttons["B"].value:
            mode = "manual"
        if speed > 1:
            speed = 1
        if speed < -1:
            speed = -1
        picoexplorer.motors[0].throttle = speed
        
        picoexplorer.set_line(4, "{} speed: {:.1}".format(mode, speed))
        
        # No faster than 10Hz
        time.sleep(.1)
