# The MIT License (MIT)
#
# Copyright (c) 2019 Bryan Siepert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit__MSA301`
================================================================================

CircuitPython library for the _MSA301 Accelerometer


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython__MSA301.git"

from time import sleep
import struct
from micropython import const
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bits import RWBits, ROBits
import adafruit_bus_device.i2c_device as i2cdevice
_MSA301_I2CADDR_DEFAULT = const(0x26)

_MSA301_REG_PARTID = const(0x01)
_MSA301_REG_OUT_X_L = const(0x02)
_MSA301_REG_OUT_X_H = const(0x03)
_MSA301_REG_OUT_Y_L = const(0x04)
_MSA301_REG_OUT_Y_H = const(0x05)
_MSA301_REG_OUT_Z_L = const(0x06)
_MSA301_REG_OUT_Z_H = const(0x07)
_MSA301_REG_MOTIONINT = const(0x09)
_MSA301_REG_DATAINT = const(0x0A)
_MSA301_REG_CLICKSTATUS = const(0x0B)
_MSA301_REG_RESRANGE = const(0x0F)
_MSA301_REG_ODR = const(0x10)
_MSA301_REG_POWERMODE = const(0x11)
_MSA301_REG_INTSET0 = const(0x16)
_MSA301_REG_INTSET1 = const(0x17)
_MSA301_REG_INTMAP0 = const(0x19)
_MSA301_REG_INTMAP1 = const(0x1A)
_MSA301_REG_TAPDUR = const(0x2A)
_MSA301_REG_TAPTH = const(0x2B)

class MSA301:
    """Driver for the MSA301 Accelerometer.

        :param ~busio.I2C i2c_bus: The I2C bus the MSA is connected to.
        :param address: The I2C device address for the sensor. Default is ``0x26``.
    """
    _part_id = ROUnaryStruct(_MSA301_REG_PARTID,"<B")

    def __init__(self, i2c_bus, address=_MSA301_I2CADDR_DEFAULT):
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, address)

        
        if (self._part_id != 0x13):
            raise AttributeError("Cannot find a MSA301")

        self.enable_all_axes()
        # // enable all axes
        # enableAxes(true, true, true);
        # // normal mode
        # setPowerMode(MSA301_NORMALMODE);
        self._power_mode = 0
        # // 500Hz rate
        # setDataRate(MSA301_DATARATE_500_HZ);
        self._data_rate = 0b1001
        # // 250Hz bw
        # setBandwidth(MSA301_BANDWIDTH_250_HZ);
        self._bandwidth = 0b1001
        # setRange(MSA301_RANGE_4_G);
        self._range = 0b01
        # setResolution(MSA301_RESOLUTION_14);
        self._resolution = 0b00

    # Register Reference:   
    # RWBits((num_bits, register_address, lowest_bit, register_width=1, lsb_first=True)
    # ROBit( register_address, bit, register_width=1, lsb_first=True)
    # UnaryStruct( register_address, struct_format)
    # https://docs.python.org/3/library/struct.html

    _disable_x = RWBit(_MSA301_REG_ODR, 7)
    _disable_y = RWBit(_MSA301_REG_ODR, 6)
    _disable_z = RWBit(_MSA301_REG_ODR, 5)

    _power_mode = RWBits(2, _MSA301_REG_POWERMODE, 6)

    _xyz_raw = ROBits(48, _MSA301_REG_OUT_X_L, 0, 6)

    _power_mode = RWBits(2, _MSA301_REG_POWERMODE, 6)

    _bandwidth = RWBits(4, _MSA301_REG_POWERMODE, 1)

    _data_rate = RWBits(4, _MSA301_REG_ODR, 0)

    _range = RWBits(2, _MSA301_REG_RESRANGE, 0)

    _resolution = RWBits(2, _MSA301_REG_RESRANGE, 2)

    @property
    def acceleration(self):
        # read the 6 bytes of acceleration data
        # zh, zl, yh, yl, xh, xl
        raw_data = self._xyz_raw
        acc_bytes = bytearray()
        # shift out bytes, reversing the order
        for shift in range(6):
            bottom_byte = (raw_data >>(8*shift) & 0xFF)
            acc_bytes.append(bottom_byte)

        # unpack three LE, signed shorts
        x, y, z = struct.unpack_from("<hhh", acc_bytes)
        
        current_range = self._range
        scale = 1.0
        if (current_range == 3):
            scale = 512.0
        if (current_range == 2):
            scale = 1024.0
        if (current_range == 1):
            scale = 2048.0
        if (current_range == 0):
            scale = 4096.0

        # shift down to the actual 14 bits and scale based on the range
        x_g = (x>>2) / scale
        y_g = (y>>2) / scale
        z_g = (z>>2) / scale

        return (x_g, y_g, z_g)

    def enable_all_axes(self):
        _disable_x = _disable_y = _disable_z = False
