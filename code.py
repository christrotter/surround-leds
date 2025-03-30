import neopixel
import config
import led_animations
import layers
 
# initialize the LEDs
leds = neopixel.NeoPixel(config.led_pin, config.num_leds, brightness=config.led_brightness, auto_write=False)
layer_leds = layers.IndicatorLEDs(leds)

# startup sequence
# led_animations.startup_sequence(leds, config.fade_time) # temporarily commented out while we build this out
startup_done = False

while True:
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
        layer_leds.set_layer_background((config.weather_colour))
        layer_leds.set_layer_right_indicator((config.RED))
        layer_leds.set_layer_top_indicator((config.CYAN))
        layer_leds.set_layer_left_indicator((config.GREEN))
        layer_leds.set_layer_pedals((config.BLUE))
    else:
        #print("No Update")
        pass
    layer_leds.show()