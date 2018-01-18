import time
from datetime import datetime as dt
from ringclock_time import RingClockTime as rct
import ringclock_animation as rca
import ringclock_mixer as rcm
import ringclock_led_base as rclb


class RingClockWork():


    def __init__(self,led=rclb.RingClockLEDBase(),static_time=None):
        # set ring sizes
        self._RING_OUT = 60
        self._RING_MID = 24
        self._RING_IN  = 12
        #init clock mode (CLASSIC/FILL)
        self._clock_mode = 'CLASSIC'
        # init LEDs
        self.led = led
        # store static time
        self.static_time = static_time
        # store the first time
        self.time_on_display = rct.create_time(None,None,None,None)
        # create empty animation list
        self.animation_list = list()
        # init clock display
        self._init_clock()
        # set clock running flag
        self._is_running = True
        print 'clockwork initialized'
        
    # shutdown clock
    def _shutdown(self):
        self.clear_pixel_buffer()
        
    # get clock state
    def get_clock_state(self):
        return self._is_running
        
    # set clock state
    def set_clock_state(self,state):
        self._is_running = state
    
    def _create_initial_animation(self,time):
        # create hands with delay, depending on clock mode
        if self._clock_mode is 'CLASSIC':
            self._create_hand(time['s'],'seconds')
            self._create_hand(time['m'],'minutes',(-time['s']))
            self._create_hand(time['h'],'hours',-(time['s']+time['m']*60))
        elif self._clock_mode is 'FILL':
            time_left_minutes = 3600 -(time['s']+time['m']*60) - 60
            time_left_hours   = 86400-(time['s']+time['m']*60+time['h']*3600)
            self._create_hand(time['s'],'seconds')
            for item in range(time['m']):
                self._create_hand(item,'minutes',time_left_minutes)
            for item in range(time['h']):
                self._create_hand(item,'hours',time_left_hours)
        else:
            raise ValueError('unknown clock mode')
        # now store the current time as displayed time
        self.time_on_display['h'] = time['h']
        self.time_on_display['m'] = time['m']
        self.time_on_display['s'] = time['s']
    
    # initializes the first animations
    def _init_clock(self):
        # create mixer instance
        self._create_mixer()
        #get the current time, if it is non static
        if self.static_time is None:
            current_time = rct.get_time()
        else:
            current_time = self.static_time
        # creat first animation
        self._create_initial_animation(current_time)
        self._process_animations(current_time)
        # calculate the colors
        self._mixer.mix_colors()
        # now show colors
        self.led.strip.show()
        
        
    def run_clock(self):
        print ('start clock')
        while (self._is_running):
            time_start = time.time()
            self._clock_tick()
            time_end = time.time()
            time_delta = time_end - time_start
            time.sleep(0.005)
            #print 'tick duration: ' + str(time_delta)
            #print time_start
            #print time_end
            print '{}:{}:{}'.format(self.time_on_display['h'],self.time_on_display['m'],self.time_on_display['s'])
            print '-------------------------'
        self._shutdown()
        print 'clock shutdown'
            

    # clear all pixel data without showing
    def clear_pixel_buffer(self):
        for i in range(self.led.COUNT):
            self.led.strip.setPixelColorRGB(i,0,0,0)
        self.led.strip.show()

    # set the color values of pixels
    def _set_pixels(self,time):
        pass

    # creates a hand depending on type
    def _create_hand(self,time,hand_type,delay=0):
        if hand_type is 'seconds':
            self.animation_list.append(rca.RingClockAnimations('fade_exp',time,'seconds',delay))
        elif hand_type is 'minutes':
            self.animation_list.append(rca.RingClockAnimations('fade_exp',time,'minutes',delay))
        elif hand_type is 'hours':
            # calculate position with respect to ring position, becasue ring positions 0 are not aligned
            if (time==12) or (time==0):
                position_mid = self._RING_OUT+self._RING_MID-1
                position_in  = self._RING_OUT+self._RING_MID+self._RING_IN-1
            else:
                position_mid = (time*2)+self._RING_OUT-1
                position_in  = time+self._RING_OUT+self._RING_MID-1
            # create hand
            self.animation_list.append(rca.RingClockAnimations('fade_exp',position_in,'hours',delay))
            self.animation_list.append(rca.RingClockAnimations('fade_exp',position_mid,'hours',delay))
            if self._clock_mode is 'FILL':
                position_mid = (time*2)+self._RING_OUT
                self.animation_list.append(rca.RingClockAnimations('fade_exp',position_mid,'hours',delay))
        else:
            raise ValueError('unknown hand')
            
    
    
    # check if a handle has changed and create an animation
    def _check_animation_required(self,time):
        if (time['s'] != self.time_on_display['s']):
            self._create_hand(time['s'],'seconds')
            # now store the current time as displayed time
            self.time_on_display['s'] = time['s']
        if (time['m'] != self.time_on_display['m']):
            self._create_hand(time['m'],'minutes')
            # now store the current time as displayed time
            self.time_on_display['m'] = time['m']
        if (time['h'] != self.time_on_display['h']):
            self._create_hand(time['h'],'hours')
            # now store the current time as displayed time
            self.time_on_display['h'] = time['h']
        
    # set the color of a pixel
    def _set_pixel_color(self,animation_obj):
        # get the brightness
        brightness = animation_obj.calculate_brightness()
        # get the pixel to animate
        pixel = animation_obj.get_pixel()
        #print 'setting brightness '+str(brightness)+' to pixel no. '+str(pixel)
        # get the color of the animation
        colors = animation_obj.get_colors()
        red = int(colors['red']*brightness)
        green = int(colors['green']*brightness)
        blue = int(colors['blue']*brightness)
        # set color
        self._mixer.add_color(pixel,red,green,blue)
    
    # process animations
    def _process_animations(self,time):
        delete_buffer = list()
        for index,item in enumerate(self.animation_list):
            # set the color of pixel
            self._set_pixel_color(item)
            # delete animation if finished
            if not item.verify_animation():
                delete_buffer.append(index)
        # now delete non valid items
        for index in sorted(delete_buffer, reverse=True):
            del self.animation_list[index]
        #print 'animation list length: '+str(len(self.animation_list))
    
    def _create_mixer(self):
        self._mixer = rcm.RingClockMixer(self.led.strip,self.led.BRIGHTNESS)
    
    # the actual clock tick function
    def _clock_tick(self):
        # create mixer instance
        self._create_mixer()
        #get the current time, if it is non static
        if self.static_time is None:
            current_time = rct.get_time()
        else:
            current_time = self.static_time
        #print time_current['h'], time_current['m'], time_current['s'], time_current['ms']
        self._check_animation_required(current_time)
        self._process_animations(current_time)
        # calculate the colors
        self._mixer.mix_colors()
        # now show colors
        self.led.strip.show()