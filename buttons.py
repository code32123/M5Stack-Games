from machine import I2C, Pin

K_UP     = 0x01
K_DOWN   = 0x02
K_LEFT   = 0x04
K_RIGHT  = 0x08
K_A      = 0x10
K_B      = 0x20
K_SELECT = 0x40
K_START  = 0x80

hardButtons = {'A':(39, 0), 'B':(38, 0), 'C':(37, 0)}


for i in hardButtons:
    hardButtons[i] = (hardButtons[i][0], Pin(hardButtons[i][0], Pin.IN))

class Buttons:
    def __init__(self, i2c, address=0x08):
        self._i2c = i2c
        self._address = address

    def getPressed(self):
        return self._i2c.readfrom(self._address, 1)[0] ^ 0xff

    def get_pressed(self):
        print("get_pressed is depreciated - drop-in getPressed")
        return self.getPressed()

    def getDown(self, button):
        if button in list(hardButtons.keys()):
            return False if hardButtons[button][1].value() == 1 else True
        else:
            return self.getPressed() & button


i2c = I2C(sda=Pin(21), scl=Pin(22))
buttons = Buttons(i2c)
