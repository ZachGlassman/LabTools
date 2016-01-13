"""
Code for communicated with SRS630 Device for measuring temperature
It mimicks the Manual.  For functions which are both read and write, there is
read flag set automatically to true.
"""
from visa import instrument


class SRS630(object):
    """Class for SRS630"""
    def __init__(self, address=19):
        self.crtl = instrument("GPID::{0}".format(address))

    def close(self):
        """close instance"""
        self.ctrl.close

    def MEAS(self, channel):
        if channel in range(0,17):
            return self.crtl.query('MEAS?{0}'.format(channel))

    def measure_multiple(self, channels):
        """measure multiple channels"""
        try:
            return [self.MEAS(i) for i in channels]
        except:
            print('Could not measure temperatures')
