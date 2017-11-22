from neopixel import *
class RingClockMixer():
    
    def __init__(self,led_strip,max_brightness=255):
        self._data   = {}
        self._strip = led_strip
        self._MAX_BRIGHTNESS = max_brightness
    
    # helper function to truncate channel if it is bigger than max brightness
    def _truncate_channel(self,value):
        if value > self._MAX_BRIGHTNESS:
            return self._MAX_BRIGHTNESS
        else:
            return value
    
    # add a color to mixer and init data if pixel is uncolored
    def add_color(self,pixel,red,green,blue):
        if pixel in self._data:
            self._data[pixel]['r'].append(red)
            self._data[pixel]['g'].append(green)
            self._data[pixel]['b'].append(blue)
        else:
            self._data[pixel] = {'r':[red],'g':[green],'b':[blue]}
    
    # mix all colors and send to stripe
    def mix_colors(self):
        for pixel in self._data:
            #calculate color values
            red   = self._truncate_channel(sum(self._data[pixel]['r']))
            green = self._truncate_channel(sum(self._data[pixel]['g']))
            blue  = self._truncate_channel(sum(self._data[pixel]['b']))
            self._strip.setPixelColorRGB(pixel,red,green,blue)
    
    # show the colors
    #def show_colors(self):
    #    self._strip.show()