				#####################
				#    Ignore this    #					
########################################################
import os, sys, time
sys.dont_write_bytecode = True
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
########################################################

from uGecko import uGecko

gecko = uGecko("192.168.1.102")
gecko.connect()

gecko.call(gecko.getSymbol("coreinit.rpl", "OSShutdown"), 1)

gecko.disconnect()

print("Done.")