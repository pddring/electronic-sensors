"""
Adventures in Electronics
* Firmware:
 - CircuitPython v9.2.1
* Hardware:
 - Raspberry pi pico in pico explorer board
 - Servo
     Pin1 (Orange	=> GP1)
     Pin2 (Red		=> 3v3)
     Pin3 (Brown	=> GND)
 - Push switch (note inverse polarity)
     Pin1 (GND 		=> 3v3)
     Pin2 (VCC		=> GND)
     Pin3 (S		=> GP0)
     
* Description:
 Reaction timer trap door of doom:
 Pico explorer board will display "Get ready" for a random amount of time
 As soon as the screen goes red, you have to press the button. If you're too slow the servo will
 open a Lego trapdoor
"""
import picoexplorer
import time
import random
import board
from digitalio import DigitalInOut, Direction, Pull

TIME_TOO_SLOW = 2
TIME_MAX_WAIT = 5

# Set up button
btn = DigitalInOut(board.GP0)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

# Open Lego servo trapdoor of doom
def open_trapdoor():
    print("Opening trapdoor")
    time.sleep(1)

# Make sure trapdoor is closed
def close_trapdoor():
    print("Closing trapdoor")
    time.sleep(1)
    
picoexplorer.init()
close_trapdoor()
while True:
    picoexplorer.set_line(3, "Get ready")
    picoexplorer.set_line(4, "")

    # random delay before pressing button
    delay = random.randint(10,30) / 10
    start_time = time.monotonic()
    duration = 0
    
    # make sure button isn't pressed too soon
    while duration < delay:
        time.sleep(0.05)
        duration = time.monotonic() - start_time
        if btn.value:
            picoexplorer.set_line(4, "Cheat!")
            open_trapdoor()
            
    # Go!
    picoexplorer.set_color(picoexplorer.COLORS_BACKGROUND_OUTER, 0xFF0000)
    picoexplorer.set_line(3, "Press button!")
    
    # Time how long it takes to press button
    start_time = time.monotonic()
    while not btn.value:
        time.sleep(0.05)
        duration = time.monotonic() - start_time
        
        # don't wait for too long
        if duration > TIME_MAX_WAIT:
            break

    # display time
    picoexplorer.set_color(picoexplorer.COLORS_BACKGROUND_OUTER, 0x000000)
    picoexplorer.set_line(3, "Time: {:.2f}s".format(duration))

    # open the trapdoor if they take too long
    if duration > TIME_TOO_SLOW:
        picoexplorer.set_line(4, "Too slow!")
        open_trapdoor()
        close_trapdoor()
    
    # if button is pressed soon enough, keep the trapdoor closed for another try
    else:
        picoexplorer.set_line(4, "Well done!")
    time.sleep(2)
