
import time
from datetime import datetime as dt

from neopixel import *


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

# get the current time
def get_time ():
    milliseconds = dt.now().microsecond / 1000
    seconds      = time.localtime()[5]
    minutes      = time.localtime()[4]
    hours        = time.localtime()[3]
    if (hours > 12):
        hours -= 12
    
    return {'ms':milliseconds,'s':seconds,'m':minutes,'h':hours}

# clear all pixel data without showing
def clear_pixel_buffer():
    for i in range(LED_COUNT):
        strip.setPixelColorRGB(i,0,0,0)

# set the color values of pixels
def set_pixels(strip,time):
    strip.setPixelColorRGB(time['h']*5,255,0,0)
    strip.setPixelColorRGB(time['m'],0,255,0)
    strip.setPixelColorRGB(time['s'],255,255,255)
    strip.setPixelColorRGB(int(time['ms']/16.7),0,0,255)
    
def clock(strip):
    #get the current time
    time_current = get_time()
    #print time_current['h'], time_current['m'], time_current['s'], time_current['ms']
    clear_pixel_buffer()
    set_pixels(strip,time_current)
    strip.show()



# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    print ('start clock')
    while True:
        time_start = dt.now()
        clock(strip)
        time_end = dt.now()
        time_delta =  (time_end.microsecond - time_start.microsecond)/1000
        time.sleep(0.01)
        print time_delta