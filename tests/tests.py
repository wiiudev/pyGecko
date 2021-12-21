from ugecko import uGecko

import time

gecko = uGecko("192.168.1.57")
#print(gecko.isConnected())
gecko.connect()

"""
print(gecko.isConnected())
print(gecko.getWiiuIp())
"""

#gecko.seriaPoke((0x105DD0A8, 0x105DD2A8), 0x00000000)

#gecko.writeString(0x121F0C94, "Hello World!" + "\x00")
#gecko.clearString(0x121F0C94, 0x121F0C94 + 32)

#print(hex(int.from_bytes(gecko.read(0x105DD0A8, 4), "big")))

#gecko.kernelWrite(0x105DD2A8, 0x3F800000)

#print(hex(gecko.kernelRead(0x105DD2A8)))

"""
print(gecko.isConsolePaused())
time.sleep(5)
gecko.pauseConsole()
print(gecko.isConsolePaused())
time.sleep(5)
gecko.resumeConsole()
print(gecko.isConsolePaused())
"""

"""
print(gecko.getServerStatus())
print(gecko.getServerVersion())
print(gecko.getOsVersion())
print(gecko.getVersionHash())
print(gecko.getAccountID())
print(gecko.getCodeHandlerAddress())
print(gecko.getDataBufferSize())
"""

#gecko.getTitleID()

#print(gecko.getSystemInformation())

"""
print(gecko.search(0x12000000, 0x13000000 - 0x12000000, 0x3F800000))
print(gecko.advancedSearch(0x12000000, 0x13000000 - 0x12000000, 0x3F800000, 0, 100000, 1))
"""

print(gecko.getEntryPointAddress())

gecko.disconnect()