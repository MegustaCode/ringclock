from datetime import datetime as dt

class RingClockTime():
    # get the current time
    @staticmethod
    def get_time ():
        time_buffer = dt.now()
        milliseconds = time_buffer.microsecond / 1000
        seconds      = time_buffer.second
        minutes      = time_buffer.minute
        hours        = time_buffer.hour
        if (hours > 12):
            hours -= 12
        return {'ms':milliseconds,'s':seconds,'m':minutes,'h':hours}
    
    @staticmethod
    def create_time(hours,minutes,seconds,milliseconds):
        return {'ms':milliseconds,'s':seconds,'m':minutes,'h':hours}
    
    # calulate time delta in float seconds
    @staticmethod
    def get_delta_seconds(time_one,time_two):
        #print time_one
        #print time_two
        buff_one = (time_one['ms']/1000.0)+time_one['s']+time_one['m']*60+time_one['h']*3600
        buff_two = (time_two['ms']/1000.0)+time_two['s']+time_two['m']*60+time_two['h']*3600
        return buff_one - buff_two
    