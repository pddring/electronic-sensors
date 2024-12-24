import board
import busio
import time
import terminalio
import displayio
import digitalio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from adafruit_motor import motor
import pwmio

PINS_PICO_EXPLORER = {"sda": board.GP20, "scl": board.GP21}

i2c = busio.I2C(**PINS_PICO_EXPLORER)
labels = []

def set_line(line, text):
    labels[line].text = text
    
def init():
    global labels
    # Release any resources currently in use for the displays
    displayio.release_displays()

    tft_cs = board.GP17
    tft_dc = board.GP16
    spi_mosi = board.GP19
    spi_clk = board.GP18
    spi = busio.SPI(spi_clk, spi_mosi)
    try:
        from fourwire import FourWire
    except ImportError:
        from displayio import FourWire

    display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
    display = ST7789(display_bus, width=240, height=240, rowstart=80, rotation=180)

    # Make the display context
    splash = displayio.Group()
    display.root_group = splash

    color_bitmap = displayio.Bitmap(240, 240, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Black

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(200, 200, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000088  # Dark blue
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
    splash.append(inner_sprite)

    # Draw a label
    text_group = displayio.Group(scale=2, x=0, y=0)
    lines = ["Adventures", "in", "Electronics", "", ""]
    y = 20
    for line in lines:
        text_area = label.Label(terminalio.FONT,
                                text=line,
                                color=0xFFFF00,
                                anchor_point=(0.5, 0.0),
                                anchored_position=(60, y))
        y += 18
        labels.append(text_area)
        text_group.append(text_area)  # Subgroup for text scaling
        
    splash.append(text_group)

# set up motors
PWM_FREQ = 50
motors = []
pwm_pins =  []
for pin in [board.GP8, board.GP9, board.GP10, board.GP11]:
    pwm_pins.append(pwmio.PWMOut(pin, frequency=PWM_FREQ))

motors.append(motor.DCMotor(pwm_pins[0], pwm_pins[1]))
motors.append(motor.DCMotor(pwm_pins[2], pwm_pins[3]))
motors[0].decay_mode= motor.SLOW_DECAY
motors[1].decay_mode= motor.SLOW_DECAY


# set up buttons
buttons = {}
button_labels = ["A", "B", "X", "Y"]
button_pins = [board.GP12, board.GP13, board.GP14, board.GP15]
for i in range(len(button_labels)):
    b = digitalio.DigitalInOut(button_pins[i])
    b.direction = digitalio.Direction.INPUT
    b.pull = digitalio.Pull.UP
    buttons[button_labels[i]] = b
    

# Used for testing new features
if __name__ == "__main__":

    while True:
        if not buttons["A"].value:
            motors[0].throttle = 1
        elif not buttons["B"].value:
            motors[0].throttle = -1
        else:
            motors[0].throttle = 0
        
        if not buttons["X"].value:
            motors[1].throttle = 1
        elif not buttons["Y"].value:
            motors[1].throttle = -1
        else:
            motors[1].throttle = 0
            
        time.sleep(.1)
        