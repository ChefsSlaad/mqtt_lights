# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
from machine import reset, Pin


print('starting garbage collector')
gc.enable()
gc.collect()
print('starting webrepl')
webrepl.start()
print('available memory {}'.format(gc.mem_free()))
