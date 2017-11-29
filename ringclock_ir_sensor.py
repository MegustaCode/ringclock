# this code is based in the pigpio ir_hasher example
import pigpio

class hasher:
    """
    This class forms a hash over the IR pulses generated by an
    IR remote.

    The remote key press is not converted into a code in the manner of
    the lirc module.  No attempt is made to decode the type of protocol
    used by the remote.  The hash is likely to be unique for different
    keys and different remotes but this is not guaranteed.

    This hashing process works for some remotes/protocols but not for
    others.  The only way to find out if it works for one or more of
    your remotes is to try it and see.

    EXAMPLE CODE

    #!/usr/bin/env python

    import time
    import pigpio
    import ir_hasher

    def callback(hash):
      print("hash={}".format(hash));

    pi = pigpio.pi()

    ir = ir_hasher.hasher(pi, 7, callback, 5)

    print("ctrl c to exit");

    time.sleep(300)

    pi.stop()
    """
    HASHTABLE = {
    2811252627:'BRIGHT_UP',
    12307315:  'BRIGHT_DOWN',
    1104437587:'OFF',
    2213358675:'ON',
    2486790203:'RED',
    3329988403:'GREEN',
    826756427: 'BLUE',
    50768435:  'WHITE',
    2961654963:'RED2',
    198230547: 'RED3',
    2025146267:'RED4',
    1879049667:'RED5',
    1393588699:'GREEN2',
    1298920555:'GREEN3',
    2963354515:'GREEN4',
    3304755411:'GREEN5',
    3659465715:'BLUE2',
    4103999155:'BLUE3',
    840884539: 'BLUE4',
    1637495115:'BLUE5',
    1678746131:'FLASH',
    2288106771:'STROBE',
    1595181691:'FADE',
    654129651: 'SMOOTH'}

    def __init__(self, pi, gpio, callback, timeout=5):

        """
        Initialises an IR remote hasher on a pi's gpio.  A gap of timeout
        milliseconds indicates the end of the remote key press.
        """

        self.pi = pi
        self.gpio = gpio
        self.code_timeout = timeout
        self.callback = callback

        self.in_code = False

        pi.set_mode(gpio, pigpio.INPUT)

        self.cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cb)

    def _hash(self, old_val, new_val):

        if   new_val < (old_val * 0.60):
            val = 13
        elif old_val < (new_val * 0.60):
            val = 23
        else:
            val = 2

        self.hash_val = self.hash_val ^ val
        self.hash_val *= 16777619 # FNV_PRIME_32
        self.hash_val = self.hash_val & ((1<<32)-1)

    def _cb(self, gpio, level, tick):

        if level != pigpio.TIMEOUT:

            if self.in_code == False:

                self.in_code = True

                self.pi.set_watchdog(self.gpio, self.code_timeout)

                self.hash_val = 2166136261 # FNV_BASIS_32

                self.edges = 1

                self.t1 = None
                self.t2 = None
                self.t3 = None
                self.t4 = tick

            else:

                self.edges += 1

                self.t1 = self.t2
                self.t2 = self.t3
                self.t3 = self.t4
                self.t4 = tick

                if self.t1 is not None:

                    d1 = pigpio.tickDiff(self.t1,self.t2)
                    d2 = pigpio.tickDiff(self.t3,self.t4)

                    self._hash(d1, d2)

        else:

            if self.in_code:

                self.in_code = False

                self.pi.set_watchdog(self.gpio, 0)

                if self.edges > 12:

                    self.callback(self.hash_val)
    
    def find_in_hashtable(self,signal):
        if signal in self.HASHTABLE:
            return True,self.HASHTABLE[signal]
        else:
            return False,None
            
class hashtable():
    
    TABLE = {
        2811252627:'BRIGHT_UP',
        12307315:  'BRIGHT_DOWN',
        1104437587:'OFF',
        2213358675:'ON',
        2486790203:'RED',
        3329988403:'GREEN',
        826756427: 'BLUE',
        50768435:  'WHITE',
        2961654963:'RED2',
        198230547: 'RED3',
        2025146267:'RED4',
        1879049667:'RED5',
        1393588699:'GREEN2',
        1298920555:'GREEN3',
        2963354515:'GREEN4',
        3304755411:'GREEN5',
        3659465715:'BLUE2',
        4103999155:'BLUE3',
        840884539: 'BLUE4',
        1637495115:'BLUE5',
        1678746131:'FLASH',
        2288106771:'STROBE',
        1595181691:'FADE',
        654129651: 'SMOOTH'
    }