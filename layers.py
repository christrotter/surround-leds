import time, random
import config
from ulab import numpy as np

# a little class to help us do a fire simulation
class IndicatorLEDs:
    def __init__(self, leds, loop_freq=config.loop_freq, update_freq=config.update_freq, fade_rgb_values=config.fade_rgb_values):
        self.leds = leds
        self.led_count = len(leds)

        # the numpy array is our temp array to mess with led values
        self.leds_numpy = np.array( leds, dtype=np.int16)  # gets length from 'leds'

        self.fade_rgb_values = np.array( (fade_rgb_values), dtype=np.int16 )
        self.last_time = time.monotonic()
        self.loop_freq = loop_freq
        self.last_update_time = self.last_time
        self.update_freq = update_freq
        self.snek_rate = 1
        self.brightness_scaler = 0.001
        self.background_sparkle = np.array( leds, dtype=np.int16 )
        self.pulse_state = 1
        self.top_pulse_state = 1
    
    def time_to_update(self):
        """
        Check if it's time to update the LEDs based on the loop frequency.
        The purpose of this is to limit CPU usage.
        :return: True if it's time to update, False otherwise.
        """
        now = time.monotonic()
        if now - self.last_time > self.loop_freq:
            self.last_time = now
            return True
        return False

    def sparkle_colour(self, color, led_range, update_num=15):
        self.leds_numpy += self.fade_rgb_values
        self.leds_numpy = np.clip(self.leds_numpy, 0,255)
        for i in range(update_num):
            self.leds_numpy[ random.randint(led_range[0],led_range[1]) ] = color
        return
    
    def pulse_colour(self, start_range, end_range, color, pulse_speed, pulse_min_percent):
        # we want to take an rgb value and pulse it - thanks, copilot
        # Calculate the pulse intensity using a sine wave - copilot killing it here
        pulse_intensity = (np.sin(self.pulse_state) + 1) / 4 + pulse_min_percent
        
        # Scale the color by the pulse intensity
        # pulsed_color = tuple(int(c * pulse_intensity) for c in color)
        pulsed_color = np.array(color) * pulse_intensity
        
        # Update the LEDs with the pulsed color
        # for i in range(start_range, end_range):
        #     self.leds_numpy[i] = pulsed_color
        self.leds_numpy[start_range:end_range] = pulsed_color #.astype(np.int16)
        
        # Increment the pulse state for the next update
        self.pulse_state += pulse_speed  # Adjust this value to control the pulse speed
        if self.pulse_state > 2 * np.pi:
            self.pulse_state -= 2 * np.pi
        return

    def alternating_yellow_black(self, fade_time=2):
        """
        Alternating yellow and black theme with a fade effect.
        Swaps yellow and black every `fade_time` seconds.
        """
        now = time.monotonic()
        # Check if it's time to swap
        if now - self.last_update_time > fade_time:
            self.last_update_time = now
            # Swap the colors
            self.background_sparkle = np.where(
                self.background_sparkle == config.YELLOW,
                (0, 0, 0),  # Black (off)
                config.YELLOW
            )

        # Apply the fade effect
        self.leds_numpy = np.clip(
            self.leds_numpy + (self.background_sparkle - self.leds_numpy) * 0.1, 0, 255
        )

        # Write the updated array to the actual LEDs
        self.leds[:] = self.leds_numpy.tolist()

    def startup_sequence(self, color, fade_time):
        # we want to fade the LEDs in to full brightness then out to black
        self.leds_numpy[0:self.led_count-1] = color
        self.leds[:] = self.leds_numpy.tolist()
        self.show()
        for i in range(int(fade_time * 1000)):
            # set the brightness of the LEDs
            self.leds.brightness = (fade_time * 500 - i) / (fade_time * 1000)
            # show the LEDs
            self.leds.show()
        return self.leds

    def set_layer_background(self, color):
        self.sparkle_colour(color, (0, self.led_count-1))
        self.leds[:] = self.leds_numpy.tolist()
        return
    
    def set_layer_top_indicator(self, color):
        # this is the zoom/meet state, maybe
        for i in range(config.top_indicator_range[0], config.top_indicator_range[1]):
            # self.leds_numpy[i] = color
            self.pulse_colour(config.top_indicator_range[0], config.top_indicator_range[1], color, 0.001, 0.15)
        self.leds[:] = self.leds_numpy.tolist()
        return    
    
    def set_layer_right_indicator(self, color):
        self.leds_numpy[config.right_indicator_range[0]:config.right_indicator_range[1]] = color
        # for i in range(config.right_indicator_range[0], config.right_indicator_range[1]):
        #     self.leds_numpy[i] = color
        self.leds[:] = self.leds_numpy.tolist()
        return
    
    def set_layer_left_indicator(self, color):
        self.leds_numpy[config.left_indicator_range[0]:config.left_indicator_range[1]] = color
        # for i in range(config.left_indicator_range[0], config.left_indicator_range[1]):
        #     self.leds_numpy[i] = color
        self.leds[:] = self.leds_numpy.tolist()
        return
    
    def set_layer_pedals(self, color):
        """
        The pedals state will flow in and update this.
        """
        for i in range(config.pedals_range_length):
            self.pulse_colour(
                config.pedals_indicator_range[0], 
                config.pedals_indicator_range[1], 
                color, 
                0.001, 
                0.15
            )
        self.leds[:] = self.leds_numpy.tolist()
        return





    # call "update()" as fast as you want
    def fire_update(self, new_color, update_num):
        # skip the loop if we are too fast
        now = time.monotonic() # each loop, get the timestamp
        if now - self.last_time < self.loop_freq:
            return
        # if we are about to execute update logic, reset the last_time to now
        self.last_time = now 
        
        # this is the fire logic: first, fade everything down, which is its own array
        # using numpy, this global fade takes 4 msec for 256 LEDs on RP2040, otherwise takes 40 msec
        # ahhhh the input here = (-1,-1,-1)
        # fire_fade = (FIRE_FADER_RED,FIRE_FADER_GREEN,FIRE_FADER_BLUE)
        # but how is this affecting the whole array of leds...
        # this is an array, a list of lists; the plus-equal must be affecting the whole array
        self.leds_numpy += self.fade_rgb_values  # fade down the working numpy array by rgb (n,n,n) values

        # ensure everything is inside 8bit; without this it will overflow
        self.leds_numpy = np.clip(self.leds_numpy, 0,255)  # constrain all elements to 0-255 # 10 lower end adds white tone
        
        # logic to fire or not fire, based on the update_freq var: if (now minus last_update_time) exceeds our update_freq, fire!
        if now - self.last_update_time > self.update_freq:
            self.last_update_time = now + random.uniform(-self.update_freq, self.update_freq)

            # format the colour properly -> turning hex into rgb
            color = (new_color>>16 & 0xff, new_color>>8 & 0xff, new_color & 0xff)  # turn color into list
            # color = (255, 85, 0)
            # update the color of only update_num count of leds to our color
            for i in range(update_num):
                # change this many LEDs: update_num
                # pick some random LEDs to update; select from our leds_numpy array(list of lists) a random selection
                # we loop over only the update_num amount of LEDs
                # so inside our loop we are picking a random selection from the list of lists and changing that RGB value
                
                self.leds_numpy[ random.randint(0,self.led_count-1) ] = color  # update random LEDs with new color
        
        # take our temp numpy array and copy it to the actual LED array
        self.leds[:] = self.leds_numpy.tolist()  # copy working numpy array to leds
        # now we are ready to show()

    def infinite_snek(self, new_color, range_length, snek_rate):
        """
        Gen'd by copilot using the doc as a guide.
        Rolling range animation: A range of LEDs is lit, and the range moves forward by 1 in each loop.
        :param new_color: Tuple (R, G, B) for the range's color.
        :param range_length: Length of the range in LEDs.
        """
        # Rate-limiting
        now = time.monotonic()
        if now - self.last_time < self.loop_freq:
            return
        self.last_time = now

        # Clear all LEDs
        self.leds_numpy[:] = (0, 0, 0)

        # Calculate the rolling range
        for i in range(range_length):
            index = (self.last_update_time + i) % self.led_count  # Wrap around using modulo
            index = int(index)
            self.leds_numpy[index] = new_color
        
        # Increment the rolling position
        self.last_update_time = (self.last_update_time + snek_rate) % self.led_count
        
        # Write the updated array to the actual LEDs
        self.leds[:] = self.leds_numpy.tolist()

    # call 'show()' whenever you want to update the actual LEDs
    def show(self):
        # this is actually the same as neopixel.NeoPixel().show()
        self.leds.show()