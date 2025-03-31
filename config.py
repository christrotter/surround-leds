import board
    
# hardware setup
led_pin = board.IO3

# main class config
loop_freq = 0.01
update_freq = 0.01
fade_rgb_values = (-1, -1, -1)  # fade down the working numpy array by rgb (n,n,n) values

right_indicator_range = (8, 84)
top_indicator_range = (120, 220)
left_indicator_range = (252, 330)
pedals_indicator_range = (450, 470)
pedals_range_length = pedals_indicator_range[1] - pedals_indicator_range[0] + 1

# effects config

fade_time = 0.25
led_brightness = 0.2
num_leds = 470 * 1

# RGB colors
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
CYCLE_TIME = 0.0001

# specific colours
weather_colour = YELLOW

fire_color_red = 0xff5500
fire_color_blue = 0x2299ff
fire_color_white = 0xffffff
fire_color_dark_grey = 0x222229
fire_color_yellow = 0xfdff33
fire_color_purple = 0x940eed
fire_color_green = 0x23ba2b
fire_color = fire_color_red

# how much to fade R,G,B each udpate
FIRE_FADER_RED = -3
FIRE_FADER_GREEN = -3
FIRE_FADER_BLUE = -3
fire_fade = (FIRE_FADER_RED,FIRE_FADER_GREEN,FIRE_FADER_BLUE)
 
# snek, by copilot
# 2   takes 9s
# 5   takes 9s
# 10  takes 10s
# 100 takes 12s
# 150 takes 14s
# 200 takes 16s
# 300 takes 20s
snek_length = 10
snek_rate = 2
snek_color = BLUE