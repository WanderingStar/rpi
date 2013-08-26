#!/usr/bin/python

import sys
import spi                        # https://github.com/lthiery/SPI-Py
from bitstring import BitArray    # https://pypi.python.org/pypi/bitstring

class Tlc59711:
    """Communicates with the TLC59711"""
    def __init__(self):
        self.outtmg = 1
        self.extgck = 0
        self.tmgrst = 1
        self.dsprpt = 1
        self.blank = 0
        self.brightness = tuple([0b1111111] * 3)  # (R, G, B) brightness
        self.pixels = [(0, 0, 0)] * 4             # (R, G, B) 0-3

    def command(self):
        """The bytes of the command that should update the data"""
        command = BitArray('0b100101') # magic WRITE code
        # make sure the values are single bits
        command += [BitArray(bool=bit) for bit in (
                self.outtmg, self.extgck, self.tmgrst,
                self.dsprpt, self.blank)]
        for b in self.brightness:
            command += BitArray(uint=b, length=7) 
        for rgb in self.pixels:
            for color in rgb:
                command += BitArray(uint=color, length=16)
        assert len(command) == 224
        return tuple([ba.uint for ba in command.cut(8)])

    def sendCommand(self, spiMode=3):
        spi.openSPI(mode=spiMode)
        spi.transfer(self.command())
        spi.closeSPI()

if __name__ == '__main__':
    tlc = Tlc59711()
    pixels = [min(65535, max(0, int(p))) for p in sys.argv[1:]]
    if len(pixels) == 1:
        tlc.pixels = [tuple(pixels) * 3] * 4
    elif len(pixels) == 3:
        tlc.pixels = [tuple(pixels)] * 4
    elif len(sys.argv) == 12:
        for i in range(4):
            tlc.pixels[i] = tuple(pixels[i*3 : i*3+3])
    else:
        print "please specify 1, 3, or 12 pixel values 0-65535"
        exit(1)
    #tlc.blank = 1
    print " ".join(["%02x" % ba for ba in tlc.command()])
    tlc.sendCommand()
