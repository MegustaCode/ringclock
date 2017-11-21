from datetime import datetime as dt

class RingClockAnimationPrototype():
    
    def __init__(self,name= 'prototype',t_in=0,t_hold=0,t_out=0): 
            self.name = name
            self.t_in = t_in 
            self.t_hold = t_hold
            self.t_out = t_out
            self.t_start = dt.time()
            self.animation_in = 'linear'
            self.animation_out = 'linear'
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
        
    # get the animation type depending on phase
    def get_animation_type(self,phase):    
        if phase is 'in':
            return self.animation_in
        elif phase is 'out':
            return self.animation_out
        elif phase is 'hold':
            raise ValueError('hold phase has no animation')
        else:
            raise ValueError('unknown phase')
    
    # get animation phase (in, hold or out)    
    def get_animation_phase(self,time):
        if (time < self.t_in):
            return 'in'
        elif ((time > self.t_in) and (time < (self.t_in + self.t_hold))):
            return 'hold'
        elif (time > (self.t_in + self.t_hold)and(time < (self.t_in+self.t_hold+self.t_out))):
            return 'out'
        else:
            raise ValueError('wrong time')
            
    # get phase time    
    def get_phase_time(self,time,phase):
        if phase is 'in':
            return time
        elif phase is 'hold':
            return time - self.t_in
        elif phase is 'out':
            return time - (self.t_in + self.t_hold)
        else:
            raise ValueError('unknown phase')
    
    # caluclate the brightness depending on the time and type
    def calculate_brightness(self,time):
        # get phase
        phase = self.get_animation_phase(time)
        # get animation type
        animation_type = self.get_animation_type(phase)
        #get phase time
        phase_time = self.get_phase_time(time,phase)
        # calculate brighntess
        if phase is 'hold':
            return self.max_brightness
        else:
            if animation_type is 'linear':
                # calculate slope
                if phase is 'in':
                    slope = self.max_brightness/self.t_in
                else:
                    slope = -self.max_brightness/self.t_out
                return slope*phase_time
            else:
                raise ValueError('unknown animation')
                
class RingClockAnimations(RingClockAnimationPrototype):
    
    def __init__(self,type_string):
        if type_string is 'simple': 
            self.RingClockAnimationPrototype('simple',0,1,0)
        elif type_string is 'fade':
            self.RingClockAnimationPrototype('fade',0.5,0.5,0.5)
        else:
            raise ValueError('unknown animation')