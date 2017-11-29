import ringclock_clockwork as rcw


class RingClockManagement():

    def __init__(self):
        print 'management initialized'
        
    def _init_clockwork(self):
        return rcw.RingClockWork()
          
# Main
if __name__ == '__main__':
    # start the manager
    manager = RingClockManagement()
    # start the clock
    clock = manager._init_clockwork()
    # start and run forever
    clock.run_clock()
    # safety
    del clock
    del manager