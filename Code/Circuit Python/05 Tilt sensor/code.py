"""
* Firmware:
 - Micropython 1.24.1
* Hardware:
 - Raspberry Pi Pico v1
 - Piezo speaker
     GP21 			=> Speaker
* Description:
 Plays audio
"""     

import pwmio
import board
import time
import picoexplorer
import keypad
import digitalio
picoexplorer.init()

picoexplorer.i2c.deinit()

""" Pins for Keypad:
GP1 GP2 GP3 GP4 GP5 GP6 GP7
C2, R1, C1, R4, R3, C3, R2
"""
rows_pins = (board.GP2, board.GP7, board.GP5, board.GP4)
cols_pins = (board.GP3, board.GP1, board.GP6)
keys = keypad.KeyMatrix(row_pins=rows_pins, column_pins=cols_pins)
KEYS = "123456789*0#"

# Replace with your own pin
pin_correct = "1234"

# Set up tilt switch
switch = digitalio.DigitalInOut(board.GP0)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.DOWN

# mario tune in musical notes and rests
tune = "E E _ E _ C E _ G"

# Create piezo buzzer PWM output.
buzzer = pwmio.PWMOut(board.GP21, variable_frequency=True)
picoexplorer.play_tune(buzzer, tune, duty_cycle=5)

pin = ""
alarm_set = True
previous_switch_value = switch.value
while True:
    # check if keypad key is pressed
    e = keys.events.get()
    if e and e.pressed:
        pin += KEYS[e.key_number]
        
        # Assume pin has 4 digits - check if correct
        if len(pin) == 4:
            if pin == pin_correct:
                alarm_set = False
                picoexplorer.play_tune(buzzer, "C G")
            else:
                alarm_set = True
                picoexplorer.play_tune(buzzer, "G C")
            pin = ""
        else:
            picoexplorer.play_tune(buzzer, "C")
        previous_switch_value = switch.value
            
    # Update alarm status
    if alarm_set:
        picoexplorer.set_line(3, "Alarm active")
        if switch.value != previous_switch_value:
            picoexplorer.set_line(3, "ALARM!")
            picoexplorer.play_tune(buzzer, "B " * 20)
            previous_switch_value = switch.value
    else:
        picoexplorer.set_line(3, "Alarm disabled")
        previous_switch_value = switch.value
    pin_masked = "*" * len(pin)
    picoexplorer.set_line(4, "Pin: [{:4}]".format(pin_masked))
    time.sleep(0.1)