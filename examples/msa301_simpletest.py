import time
import board
import adafruit_msa301
i2c = board.I2C()

msa = adafruit_msa301.MSA301(i2c)
while True:
    print("%f %f %f"%msa.acceleration)
    time.sleep(0.0125)
