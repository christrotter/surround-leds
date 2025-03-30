import time, random
import config
from ulab import numpy as np

# a little class to help us do a fire simulation
class FireLEDs:
    def __init__(self,leds, fade_by, update_rate=0.000001, fire_rate=0.00001, chase_rate=0.05):
        self.leds = leds
        self.led_count = len(leds)

        # the numpy array is our temp array to mess with led values
        self.leds_numpy = np.array( leds, dtype=np.int16)  # gets length from 'leds'

        self.fade_by = np.array( fade_by, dtype=np.int16 )
        self.last_time = time.monotonic()
        self.update_rate = update_rate
        self.chase_rate = chase_rate
        self.last_fire_time = self.last_time
        self.fire_rate = fire_rate
        self.snek_rate = 1
        self.brightness_scaler = 0.001

    # call "update()" as fast as you want
    def fire_update(self, new_color, update_num):
        # skip the loop if we are too fast
        now = time.monotonic() # each loop, get the timestamp
        if now - self.last_time < self.update_rate:
            return
        # if we are about to execute update logic, reset the last_time to now
        self.last_time = now 
        
        # this is the fire logic: first, fade everything down, which is its own array
        # using numpy, this global fade takes 4 msec for 256 LEDs on RP2040, otherwise takes 40 msec
        # ahhhh the input here = (-1,-1,-1)
        # fire_fade = (FIRE_FADER_RED,FIRE_FADER_GREEN,FIRE_FADER_BLUE)
        # but how is this affecting the whole array of leds...
        # this is an array, a list of lists; the plus-equal must be affecting the whole array
        self.leds_numpy += self.fade_by  # fade down the working numpy array by rgb (n,n,n) values
                
        # ensure everything is inside 8bit; without this it will overflow
        self.leds_numpy = np.clip(self.leds_numpy, 0,255)  # constrain all elements to 0-255 # 10 lower end adds white tone
        
        # logic to fire or not fire, based on the fire_rate var: if (now minus last_fire_time) exceeds our fire_rate, fire!
        if now - self.last_fire_time > self.fire_rate:
            self.last_fire_time = now + random.uniform(-self.fire_rate, self.fire_rate)

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
        if now - self.last_time < self.update_rate:
            return
        self.last_time = now

        # Clear all LEDs
        self.leds_numpy[:] = (0, 0, 0)

        # Calculate the rolling range
        for i in range(range_length):
            index = (self.last_fire_time + i) % self.led_count  # Wrap around using modulo
            index = int(index)
            self.leds_numpy[index] = new_color
        
        # Increment the rolling position
        self.last_fire_time = (self.last_fire_time + snek_rate) % self.led_count
        
        # Write the updated array to the actual LEDs
        self.leds[:] = self.leds_numpy.tolist()

    # call 'show()' whenever you want to update the actual LEDs
    def show(self):
        # this is actually the same as neopixel.NeoPixel().show()
        self.leds.show()