from datetime import datetime as dt
from ringclock_time import RingClockTime as rct
from math import log

class RingClockAnimationPrototype():
    
    def __init__(self,name,pixel,t_in,t_hold,t_out,red=1,green=1,blue=1): 
            self.name = name
            self.t_in = t_in 
            self.t_hold = t_hold
            self.t_out = t_out
            self.t_start = rct.get_time()
            self.animation_in = 'linear'
            self.animation_out = 'linear'
            self.pixel = pixel
            self.phase = 'in'
            self.colors = {'red':red,'green':green,'blue':blue}
            # define parameters
            self.max_brightness = 255
            
#    def set_name(self,string):
#            self.name = string
#    
#    def set_t_in(self,time):
#        self.t_in = time
#        
#    def set_t_hold(self,time):
#        self.t_hold = time
#        
#    def set_t_out(self,time):
#        self.t_out = time
#        
#    def set_t_start(self,time):
#        self.t_start = time
    def get_colors(self):
        return self.colors
    
    def get_pixel(self):
        return self.pixel
    
    def _get_start_time(self):
        return self.t_start
    
    def _get_phase(self):
        return self.phase
    
    def _set_phase(self,phase):
        self.phase = phase
    
    def verify_animation(self):
        if self._get_phase() is 'done':
            return False
        else:
            return True
        
    # get the animation type depending on phase
    def _get_animation_type(self,phase):    
        if phase is 'in':
            return self.animation_in
        elif phase is 'out':
            return self.animation_out
        elif phase is ('hold'or'done'):
            raise ValueError('hold or done phase have no animation')
        else:
            raise ValueError('unknown phase')
    
    # get animation phase (in, hold or out)    
    def _get_animation_phase(self,time):
        if (time <= self.t_in):
            #print 'phase: in'
            return 'in'
        elif ((time > self.t_in) and (time < (self.t_in + self.t_hold))):
            #print 'phase: hold'
            return 'hold'
        elif (time > (self.t_in + self.t_hold)and(time < (self.t_in+self.t_hold+self.t_out))):
            #print 'phase: out'
            return 'out'
        else:
            #print 'phase: done'
            return 'done'
            #raise ValueError('wrong time')
            
    # get phase time    
    def _get_phase_time(self,time,phase):
        if phase is 'in':
            return time
        elif phase is 'hold':
            return time - self.t_in
        elif phase is 'out':
            return time - (self.t_in + self.t_hold)
        else:
            raise ValueError('unknown phase')
            
    def _calculate_linear_brightness(self,phase,phase_time):
        # calculate slope, but catch if t=0! If in in, 
        # brighntess is max otherwise it is zero
        try:
            if phase is 'in':
                slope = self.max_brightness/self.t_in
                return int(slope*phase_time)
            else:
                slope = -self.max_brightness/self.t_out
                return int(slope*phase_time) + self.max_brightness
        except ZeroDivisionError:
            if phase is 'in':
                return self.max_brightness
            else:
                return 0
    def _calculate_exp_brightness(self,phase,phase_time):
        if phase is 'in':
            y=(2**(phase_time/((self.t_in*log(2))/log(self.max_brightness))))-1
        elif phase is 'out':
            y=-(2**(phase_time/((self.t_out*log(2))/log(self.max_brightness))))-1
        else:
            raise ValueError('unknown phase')
        return y
            
    # caluclate the brightness depending on the time and type
    def calculate_brightness(self):
        # get the time delta between creation and now
        time_delta = rct.get_delta_seconds(rct.get_time(),self._get_start_time())
        #print 'time delta: ' + str(time_delta)
        # get phase
        phase = self._get_animation_phase(time_delta)
        # store phase for later use
        self._set_phase(phase)
        # calculate brightness depending on phase
        if phase is 'hold':
            return self.max_brightness
        elif phase is 'done':
            return 0
        else:
            # get animation type
            animation_type = self._get_animation_type(phase)
            #get phase time
            phase_time = self._get_phase_time(time_delta,phase)
            if animation_type is 'linear':
                return self._calculate_linear_brightness(phase,phase_time)
            elif animation_type is 'exp':
                return self._calculate_exp_brightness(phase,phase_time)
            else:
                raise ValueError('unknown animation')
                
class RingClockAnimations(RingClockAnimationPrototype):
    
    def __init__(self,type_string,pixel,hand):
        if hand is 'seconds':
            red   = 1
            green = 0
            blue  = 0
            if type_string is 'simple':
                hold_period = 1
            elif type_string is 'fade':
                hold_period = 0.5
            elif type_string is 'fade_exp':
                hold_period = 0.5
            else:
                raise ValueError('unknown animation')
        elif hand is 'minutes':
            red   = 0
            green = 1
            blue  = 0
            hold_period = 60
        elif hand is 'hours':
            red   = 0
            green = 0
            blue  = 1
            hold_period = 3600
        else:
            raise ValueError('unknown hand')
            
        if type_string is 'simple':
            RingClockAnimationPrototype.__init__(self,type_string,pixel,0,hold_period,0,red,green,blue)
        elif type_string is 'fade':
            RingClockAnimationPrototype.__init__(self,type_string,pixel,0.5,hold_period,0.4,red,green,blue)
        elif type_string is 'fade_exp':
            RingClockAnimationPrototype.__init__(self,type_string,pixel,0.5,hold_period,2,red,green,blue)
        else:
            raise ValueError('unknown animation')