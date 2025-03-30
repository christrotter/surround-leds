import neopixel
import fire
import config
import led_animations
from rainbowio import colorwheel
import time
import layers
 
# initialize the LEDs
leds = neopixel.NeoPixel(config.led_pin, config.num_leds, brightness=config.led_brightness, auto_write=False)
fire_leds = fire.FireLEDs(leds, fade_by=config.fire_fade)
layer_leds = layers.IndicatorLEDs(leds)

# startup sequence
# led_animations.startup_sequence(leds, config.fade_time)
startup_done = False

while True:
    # fire_leds.fire_update( colorwheel(time.monotonic()*40), 30 )  # rainbow fire
    # fire_leds.fire_update( (config.fire_color), 30 )  # standard fire effect
    # fire_leds.infinite_snek( (config.snek_color), config.snek_length , config.snek_rate)
    # nullify startup sequence brightness modification
    if startup_done is False:
        if leds.brightness < config.led_brightness:
            print("updating brightness")
            leds.brightness = leds.brightness + 0.001
        else:
            print("done updating brightness")
            # comment
            startup_done = True
    if layer_leds.time_to_update() is True:
        #print("Yes Update")
        layer_leds.set_layer_background((config.BLUE))
        layer_leds.set_layer_right_indicator((config.RED))
        layer_leds.set_layer_top_indicator((config.CYAN))
        layer_leds.set_layer_left_indicator((config.GREEN))
        layer_leds.set_layer_pedals((config.YELLOW))
    else:
        #print("No Update")
        pass
    layer_leds.show()