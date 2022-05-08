from ugecko import uGecko

gecko = uGecko("192.168.1.57")
gecko.connect()

print(gecko.kernelRead(0x10000000))

gecko.disconnect()

print("Done.")