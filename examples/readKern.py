				#####################
				#    Ignore this    #					
########################################################
import os, sys
sys.dont_write_bytecode = True
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
########################################################

from uGecko import uGecko

gecko = uGecko("192.168.1.102")
gecko.connect()

print(gecko.kernelRead(0x10000000))

gecko.disconnect()

print("Done.")