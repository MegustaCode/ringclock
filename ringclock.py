import time
#import ringclock_animation as rc_ani
from datetime import datetime as dt

from neopixel import *

class RingClock():

    # LED strip configuration:
    LED_COUNT      = 60      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL, self.LED_STRIP)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        
    def start_clock(self):
        print ('start clock')
        while True:
            time_start = dt.now()
            self.clock()
            time_end = dt.now()
            time_delta =  (time_end.microsecond - time_start.microsecond)/1000
            #time.sleep(0.01)
            print time_delta        
        
    
    # get the current time
    @staticmethod
    def get_time ():
        milliseconds = dt.now().microsecond / 1000
        seconds      = time.localtime()[5]
        minutes      = time.localtime()[4]
        hours        = time.localtime()[3]
        if (hours > 12):
            hours -= 12
        return {'ms':milliseconds,'s':seconds,'m':minutes,'h':hours}

    # clear all pixel data without showing
    def clear_pixel_buffer(self):
        for i in range(self.LED_COUNT):
            self.strip.setPixelColorRGB(i,0,0,0)

    # set the color values of pixels
    def set_pixels(self,time):
        self.strip.setPixelColorRGB(time['h']*5,255,0,0)
        self.strip.setPixelColorRGB(time['m'],0,255,0)
        self.strip.setPixelColorRGB(time['s'],255,255,255)
        self.strip.setPixelColorRGB(int(time['ms']/16.7),0,0,255)

    #def check_animation_required(time):

    def clock(self):
        #get the current time
        time_current = self.get_time()
        #print time_current['h'], time_current['m'], time_current['s'], time_current['ms']
        self.clear_pixel_buffer()
        self.set_pixels(time_current)
        self.strip.show()



# Main program logic follows:
if __name__ == '__main__':
    foo = RingClock()
    foo.start_clock()