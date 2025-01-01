"""
* Firmware:
 - Micropython 1.24.1
* Hardware:
 - Raspberry Pi Pico v1
 - Piezo speaker
     GP0 			=> Speaker
* Description:
 Plays audio
"""     

import pwmio
import board
import time
import picoexplorer
picoexplorer.init()

# Define a list of tones/music notes to play.
NOTE_LENGTH = 0.2
TIME_BETWEEN_NOTES = 0.02
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
ON = 10
OFF = 0
tune = "C D E D C D E D C D E2 C2 C2"

# Create piezo buzzer PWM output.
buzzer = pwmio.PWMOut(board.GP0, variable_frequency=True)

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
        buzzer.duty_cycle = ON
    print("Playing {} for {} at {} Hz".format(note_name, note_length, note_frequency))
    time.sleep(NOTE_LENGTH * note_length)  
    buzzer.duty_cycle = OFF
    time.sleep(TIME_BETWEEN_NOTES)
    