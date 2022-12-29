# Complete project details at https://RandomNerdTutorials.com

from machine import Pin, ADC
from time import sleep

# Valid Pins: 2, 25, 26, 35, 36

pot = ADC(Pin(2))
pins = []
for x in [1,2,3,5,16,17,18,19,21,22,23,25,26,35,36]:
  try:
    pins.append((x,ADC(Pin(x))))
  except ValueError:
    pins.append("ERROR")
print(pins)
# pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v

# while True:
#   pot_value = pot.read()
#   print(pot_value)
#   sleep(0.1)