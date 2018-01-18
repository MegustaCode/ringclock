import ringclock_clockwork    as rcw
import ringclock_ir_sensor    as rcir
import ringclock_lamp         as rcl
import ringclock_helpers      as rch
import ringclock_light_sensor as rcls
import ringclock_led_base     as rclb
import ringclock_time         as rct
import pigpio

class RingClockManagement():
    
    PIN_IR_SENSOR = 17
    MAX_DYNAMIC_BRIGHTNESS = 200.0
    MIN_DYNAMIC_BRIGHTNESS = 50
    MAX_LUX = 10000
    MIN_LUX = 10
    # TODO: create non-linear brightness curve
    BRIGHTNESS_COEFFICIENT = (MIN_DYNAMIC_BRIGHTNESS-MAX_DYNAMIC_BRIGHTNESS)/(MAX_LUX-MIN_LUX)
    LIGHT_SENSOR_PERIOD = 1
    

    def __init__(self):
        # inits LEDs
        self.led = rclb.RingClockLEDBase()
        # init pigpio
        self.gpio = pigpio.pi()
        # init IR sensor
        self.ir = rcir.hasher(self.gpio, self.PIN_IR_SENSOR, self._callback_hasher, 5)
        # set state
        self.state = 'CLOCK'
        # init light sensor
        self.light_sensor = rcls.RingClockLightSensor()
        # init thread which periodically reads light sensor
        self.light_sensor_thread = rch.PeriodicThread(self._light_sensor_callback,self.LIGHT_SENSOR_PERIOD)
        self.light_sensor_thread.start()
        print 'management initialized'
        
        
    def init_clockwork(self):
        #time = rct.RingClockTime.create_time(11,59,0,0)
        #return rcw.RingClockWork(static_time=time)
        return rcw.RingClockWork(led=self.led)
    
    # callback function of the light sensor thread
    def _light_sensor_callback(self):
        value = self.light_sensor.get_luminosity()
        new_brightness = int(self._calculate_brightness(value))
        self.led.set_brightness(new_brightness)
        print 'current lux: {}, new brightness set to {}'.format(value,new_brightness)
        
    # calculate the brightness depending on lux level
    def _calculate_brightness(self,lux):
        if lux > self.MAX_LUX:
            return self.MIN_DYNAMIC_BRIGHTNESS
        elif lux < self.MIN_LUX:
            return self.MAX_DYNAMIC_BRIGHTNESS
        else:
            return self.BRIGHTNESS_COEFFICIENT*lux+self.MAX_DYNAMIC_BRIGHTNESS
            
    
    def _callback_hasher(self,hash):
        hash_found, name = self.ir.find_in_hashtable(hash)
        if name is 'ON':
            # shutdown clock 
            self.clock.set_clock_state(False)
            # set state to LAMP
            self.state = 'LAMP'
        elif name is 'OFF':
            self.state = 'CLOCK'
            self.lamp.set_last_button('OFF')
        elif name is None:
            print 'unknown button'
        else:
            try:
                self.lamp.set_last_button(name)
            except AttributeError:
                print 'button {} pushed without lamp being activated'.format(name)
        
# Main
if __name__ == '__main__':
    
    # init the manager
    manager  = RingClockManagement()
    # loop
    no_error = True
    while(no_error):
        if manager.state is 'CLOCK':
            # start the clock
            manager.clock = manager.init_clockwork()
            manager.clock.run_clock()
        elif manager.state is 'LAMP':
            manager.lamp = rcl.RingClockLamp()
            manager.lamp.run()
        else:
            print 'unknown state'
    
    #foo.on_event('next')
#     # start the manager
#     manager = RingClockManagement()
#     # start the clock
#     manager.clock = manager._init_clockwork()
#     # start and run forever
#     manager.clock.run_clock()
#     # safety
#     #del clock
#     #del manager
    