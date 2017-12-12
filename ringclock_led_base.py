
from neopixel import *

class RingClockLEDBase():
    # LED strip configuration:
    COUNT      = 96      # Number of LED pixels.
    PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    DMA        = 5       # DMA channel to use for generating signal (try 5)
    BRIGHTNESS = 125     # Set to 0 for darkest and 255 for brightest
    INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.COUNT, self.PIN, self.FREQ_HZ, self.DMA, self.INVERT, self.BRIGHTNESS, self.CHANNEL, self.STRIP)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        print 'led base initialized'