"""
Firmware:
- Micropython 1.24.1
Hardware:
- Raspberry Pi Pico v1
- 18B20 temperature and humidity sensor
    Pin 1 (G)	=> GND
    Pin 2 (R)	=> 3.3v
    Pin 3 (Y)	=> GP0
Description:
- Reads temperature ('C) each second
"""

import machine, onewire, ds18x20, time

ds_pin = machine.Pin(0)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

while True:
  ds_sensor.convert_temp()
  for rom in roms:
    # convert to id to hex
    s = "".join([hex(b)[2:] for b in rom])
    
    print("Sensor 0x{}: {}'C".format(s, ds_sensor.read_temp(rom)))
  time.sleep(1)
