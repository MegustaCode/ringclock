import ringclock_clockwork as rcw
import ringclock_ir_sensor as rcir
import pigpio


class RingClockManagement():
    
    PIN_IR_SENSOR = 17

    def __init__(self):
        # init pigpio
        self.gpio = pigpio.pi()
        # init IR sensor
        self.ir = rcir.hasher(self.gpio, self.PIN_IR_SENSOR, self._callback_hasher, 5)
        
        print 'management initialized'
        
    def _init_clockwork(self):
        return rcw.RingClockWork()
    
    def _callback_hasher(self,hash):
        hash_found, name = self.ir.find_in_hashtable(hash)
        if name is 'ON':
            # shutdown clock 
            self.clock.set_clock_state(False)
        
          
# Main
if __name__ == '__main__':
    # start the manager
    manager = RingClockManagement()
    # start the clock
    manager.clock = manager._init_clockwork()
    # start and run forever
    manager.clock.run_clock()
    # safety
    #del clock
    #del manager
    