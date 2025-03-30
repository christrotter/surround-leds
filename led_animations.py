import config
import time
import fire
from rainbowio import colorwheel
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import MAGENTA, ORANGE, TEAL
from adafruit_led_animation.animation.sparklepulse import SparklePulse

def startup_sequence(leds, fade_time):
    color_chase(leds, config.RED, config.CYCLE_TIME)  # Increase the number to slow down the color chase
    fade_leds(leds, -1, config.fade_time)

def fade_leds(leds, direction, fade_time):
    for i in range(int(fade_time * 1000)):
        # set the brightness of the LEDs
        leds.brightness = (fade_time * 500 - i) / (fade_time * 1000)
        # show the LEDs
        leds.show()
    return leds

# color_chase(RED, CYCLE_TIME)  # Increase the number to slow down the color chase
def color_chase(leds, color, wait):
    """
    Over each loop, it advances a colour bar by one LED.
    """
    # now do the snake animation - move the colour bar one led per cycle
    for i in range(config.num_leds):
        # set the current led to the colour
        leds[i] = color
        # set the previous led to black
        if i > 0:
            leds[i - 40] = 0x000000
        # show the LEDs
        leds.show()
        # wait a bit before moving on
        time.sleep(wait)
    return

# rainbow_cycle(CYCLE_TIME)  # Increase the number to slow down the rainbow
def rainbow_cycle(leds, wait):
    for j in range(255):
        for i in range(config.num_leds):
            rc_index = (i * 256 // config.num_leds) + j
            leds[i] = colorwheel(rc_index & 255)
        leds.show()
        time.sleep(wait)

def colorwheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    MULTIPLIER = 3
    if pos < 0 or pos > 255:
        return (0, 0, 0, 0)
    if pos < 85:
        return (255 - pos * MULTIPLIER, pos * MULTIPLIER, 0, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * MULTIPLIER, pos * MULTIPLIER, 0)
    pos -= 170
    return (pos * MULTIPLIER, 0, 255 - pos * MULTIPLIER, 0)