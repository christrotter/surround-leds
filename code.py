import neopixel
import config
import led_animations
import layers
import board

# initialize the LEDs
leds = neopixel.NeoPixel(config.led_pin, config.num_leds, brightness=config.led_brightness, auto_write=False)
layer_leds = layers.IndicatorLEDs(leds)

import busio
import digitalio
from adafruit_httpserver import Server, Request, Response
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socketpool as socketpool

def set_up_server(eth):
    pool = socketpool.SocketPool(eth)
    server = Server(pool, "/static", debug=True)
    
    @server.route("/")
    def base(request: Request):
        """
        Serve a default static plain text message.
        """
        return Response(request, "Hello from the CircuitPython HTTP Server!")
    return server
    # server = pool.socket()  # Allocate socket for the server
    # server_ip = eth.pretty_ip(eth.ip_address)  # IP address of server
    # server_port = 50007  # Port to listen on
    # server.bind((server_ip, server_port))  # Bind to IP and Port
    # server.listen()  # Begin listening for incoming clients 
    # print(f"Accepting connections on {server_ip}:{server_port}")

def set_up_eth():
    print("Setting up network server...")
    cs = digitalio.DigitalInOut(board.IO14)
    spi_bus = busio.SPI(board.IO13, MOSI=board.IO11, MISO=board.IO12)
    eth = WIZNET5K(spi_bus, cs)
    return eth


def listen_for_inputs(server, eth):
    # conn, addr = server.accept()  # Wait for a connection from a client.
    # print(f"Connection accepted from {addr}, reading exactly 1024 bytes from client")
    # with conn:
    #     data = conn.recv(1024)
    #     if data:  # Wait for receiving data
    #         print(data)
    #         conn.send(data)  # Echo message back to client
    # print("Connection closed")
    server.serve_forever(str(eth.pretty_ip(eth.ip_address)))

# startup sequence
eth = set_up_eth()
server = set_up_server(eth)
# led_animations.startup_sequence(leds, config.fade_time) # temporarily commented out while we build this out
layer_leds.startup_sequence(config.RED, config.fade_time)
startup_done = False

while True:
    # nullify startup sequence brightness modification
    if startup_done is False:
        if leds.brightness < config.led_brightness:
            #print("updating brightness")
            leds.brightness = leds.brightness + 0.02
        else:
            print("Done updating brightness")
            # comment
            startup_done = True
    listen_for_inputs(server, eth)
    if layer_leds.time_to_update() is True:
        #print("Yes Update")
        layer_leds.set_layer_background((config.weather_colour))
        # layer_leds.set_layer_right_indicator((config.RED))
        layer_leds.set_layer_top_indicator((config.CYAN))
        # layer_leds.set_layer_left_indicator((config.GREEN))
        layer_leds.set_layer_pedals((config.BLUE))
    else:
        #print("No Update")
        pass
    layer_leds.show()