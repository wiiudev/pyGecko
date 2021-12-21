from ugecko import uGecko

gecko = uGecko("192.168.1.57")
gecko.connect()

# 550 -> 5.5.X
print(gecko.getOsVersion())

gecko.disconnect()

print("Done.")