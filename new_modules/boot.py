# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
from machine import reset, Pin

validpins = (0, 2, 4, 5, 12, 13, 14, 15)

print('turning off all pins')
for p in validpins:
    pin = Pin(p, Pin.OUT)
    pin.value(0)
    print('pin {} off'.format(p), end=' ')
print()
    
print('starting webrepl')
webrepl.start()
print('starting garbage collector')
gc.enable()
gc.collect()
