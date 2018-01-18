from neopixel import *
class RingClockMixer():
    
    def __init__(self,led_strip_obj,led_obj):
        self._data     = {}
        self._strip    = led_strip_obj
        self._led      = led_obj
        self._mix_type = 'sum' 
        
    # get the curretn max brighntess from the LED object
    def _get_max_brightness(self):
        return self._led.get_brightness()
    
    # helper function to truncate channel if it is bigger than max brightness
    def _truncate_channel(self,value):
        if value > self._get_max_brightness():
            return self._get_max_brightness()
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
            if self._mix_type is 'sum':
                red   = self._truncate_channel(sum(self._data[pixel]['r']))
                green = self._truncate_channel(sum(self._data[pixel]['g']))
                blue  = self._truncate_channel(sum(self._data[pixel]['b']))
            elif self._mix_type is 'average':
                red   = sum(self._data[pixel]['r'])/len(self._data[pixel]['r'])
                green = sum(self._data[pixel]['g'])/len(self._data[pixel]['g'])
                blue  = sum(self._data[pixel]['b'])/len(self._data[pixel]['b'])
            else:
                raise ValueError('unknown mixing type')
            #print '# ' +str(pixel)+'|'+str(red)+'|'+str(green)+'|'+str(blue)
            self._strip.setPixelColorRGB(pixel,red,green,blue)
            
    def clear_data(self):
        self._data = {}
            
                                         
    
    # show the colors
    def show_colors(self):
        self._strip.show()
        
    # clear display
    def clear_display(self):
        for item in range(self_strip.COUNT):
            self._strip.setPixelColorRGB(item,0,0,0)
        self.show_colors()