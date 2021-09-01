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

titleID = 0x0005000010176A00 # Splatoon EUR
CheckTitleID = gecko.getSymbol("sysapp.rpl", "SYSCheckTitleExists")
exist = gecko.call(CheckTitleID, titleID >> 32, titleID & 0xFFFFFFFF)

if exist: # The game is on the WiiU
	gecko.call(gecko.getSymbol("sysapp.rpl", "SYSLaunchTitle"), titleID >> 32, titleID & 0xFFFFFFFF)
	print("Game switched.")
else:
	print(f"The game has not been detected on the WiiU!")

gecko.disconnect()

print("Done.")