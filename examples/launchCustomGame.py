from ugecko import uGecko

gecko = uGecko("192.168.1.57")
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