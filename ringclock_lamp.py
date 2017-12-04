import ringclock_mixer as rcm
import ringclock_led_base as rclb


class RingClockLamp():
    
    def __init__(self):
        # init LEDs
        self.led = rclb.RingClockLEDBase()
        
        self._mode  = 'COLOR'
        self._color = 'RED'
        self._last_button = 'ON'
        self._button_active = False
        self.mixer  = rcm.RingClockMixer(self.led.strip)
        self._brightness = self.led.BRIGHTNESS
        self._stepsize = 50
        
        print 'lamp initialized'
        
#     def set_mode(self,mode):
#         self._mode = mode
        
#     def set_color(self,color):
#         self._color = color
        
    def set_last_button(self,button):
        self._last_button = button
        self._button_active = True
        
    def _claclulate_brightness(self):
        # increase/deacrease brightness
        if self._last_button is 'BRIGHT_UP':
            self._brightness += self._stepsize
            print 'increasing brightness'
        else:
            self._brightness -= self._stepsize
            print 'decreasing brightness'
        # fix if value is too high/low
        if self._brightness > self.led.BRIGHTNESS:
            self._brightness = self.led.BRIGHTNESS
        elif self._brightness < 0:
            self._brightness = 0
        
    def _handle_button(self):
        if self._last_button is 'ON':
            pass
        elif self._last_button is 'OFF':
            self._mode = 'OFF'
            pass
        elif self._last_button is 'BRIGHT_UP':
            self._claclulate_brightness()
        elif self._last_button is 'BRIGHT_DOWN':
            self._claclulate_brightness()
        elif self._last_button is 'FLASH':
            pass
        elif self._last_button is 'STROBE':
            pass
        elif self._last_button is 'FADE':
            pass
        elif self._last_button is 'SMOOTH':
            pass
        # should only be a color
        else:
            self._color = self._last_button
        
    def run(self):
        while(True):
            # handle button presses
            if self._button_active:
                self._handle_button()
                self._button_active = False
                print 'button pushed: {}'.format(self._last_button)
            # handle modes
            if self._mode is 'COLOR':
                self._mode_color()
            if self._mode is 'OFF':
                print 'shutting down lamp'
                break
    
    def _mode_color(self):
        self.mixer.clear_data()
        if self._color is 'RED':
            for pixel in range(self.led.COUNT):
                self.mixer.add_color(pixel,self._brightness,0,0)
        elif self._color is 'GREEN':
            for pixel in range(self.led.COUNT):
                self.mixer.add_color(pixel,0,self._brightness,0)
        elif self._color is 'BLUE':
            for pixel in range(self.led.COUNT):
                self.mixer.add_color(pixel,0,0,self._brightness)
        elif self._color is 'WHITE':
            for pixel in range(self.led.COUNT):
                self.mixer.add_color(pixel,self._brightness,self._brightness,self._brightness)
        
        self.mixer.mix_colors()    
        self.led.strip.show()
        