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

pin_correct = "1234"

# Define a list of tones/music notes to play.
NOTES = {
    "C": 261,
    "C#": 277,
    "Db": 277,
    "D": 294,
    "D#": 311,
    "Eb": 311,
    "E": 330,
    "F": 349,
    "F#": 370,
    "Gb": 370,
    "G": 392,
    "G#": 415,
    "Ab": 415,
    "A": 440,
    "A#": 466,
    "Bb": 466,
    "B": 494
    }

MAX_VOLUME = 2**15
ON = MAX_VOLUME
OFF = 0
# mario tune :)
tune = "E E _ E _ C E _ G"

# Create piezo buzzer PWM output.
buzzer = pwmio.PWMOut(board.GP21, variable_frequency=True)

# play a tune (e.g. "E E _ E _ C E _ G")  on a pwm pin (buzzer) 
def play_tune(buzzer, tune, time_each_note=0.1, time_between_notes=0.01, duty_cycle=2**15):
    # Main loop will go through each tone in order up and down.
    notes = tune.split(" ")
    for note in notes:
        # Play tones going from start to end of list.
        note_length = note[-1]
        if note_length in "0123456789":
            note_length = int(note_length)
            note_name = note[0:-1]
        else:
            note_length = 1
            note_name = note
        note_frequency = 0
        
        # _ means rest
        if note_name != "_":
            note_frequency = NOTES[note_name]
            buzzer.frequency = note_frequency * 2
            buzzer.duty_cycle = duty_cycle
        time.sleep(time_each_note * note_length)  
        buzzer.duty_cycle = 0
        time.sleep(time_between_notes)

play_tune(buzzer, tune, duty_cycle=5)
pin = ""
alarm_set = True

while True:
    if alarm_set:
        picoexplorer.set_line(3, "Alarm active")
    else:
        picoexplorer.set_line(3, "Alarm disabled")
        
    e = keys.events.get()
    if e and e.pressed:
        pin += KEYS[e.key_number]
        if len(pin) == 4:
            if pin == pin_correct:
                alarm_set = False
                play_tune(buzzer, "C G")
            else:
                alarm_set = True
                play_tune(buzzer, "G C")
            pin = ""
        else:
            play_tune(buzzer, "C")
    pin_masked = "*" * len(pin)
    picoexplorer.set_line(4, "Pin: [{:4}]".format(pin_masked))
    time.sleep(0.1)
    