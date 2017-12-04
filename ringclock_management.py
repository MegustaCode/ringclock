import ringclock_clockwork as rcw
import ringclock_ir_sensor as rcir
import ringclock_lamp      as rcl
import pigpio

class RingClockManagement():
    
    PIN_IR_SENSOR = 17

    def __init__(self):
        # init pigpio
        self.gpio = pigpio.pi()
        # init IR sensor
        self.ir = rcir.hasher(self.gpio, self.PIN_IR_SENSOR, self._callback_hasher, 5)
        # set state
        self.state = 'CLOCK'
        print 'management initialized'
        
        
    def init_clockwork(self):
        return rcw.RingClockWork()
    
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
            self.lamp.set_last_button(name)

        
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
    