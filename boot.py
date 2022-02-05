# This file is executedon every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()


import snakey, time

while True:
	snakey.main()
	time.sleep(0.01)

# import bitmapTest
# bitmapTest.main()