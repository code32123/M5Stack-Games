from machine import I2C, Pin

K_B      = 0x20
K_DOWN   = 0x02
K_LEFT   = 0x04
K_RIGHT  = 0x08
K_UP     = 0x01
K_A      = 0x10
K_SELECT = 0x40
K_START  = 0x80

class Buttons:
    def __init__(self, i2c, address=0x08):
        self._i2c = i2c
        self._address = address

    def get_pressed(self):
        return self._i2c.readfrom(self._address, 1)[0] ^ 0xff


i2c = I2C(sda=Pin(21), scl=Pin(22))
buttons = Buttons(i2c)