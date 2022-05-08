from ugecko import uGecko

gecko = uGecko("192.168.1.57")
gecko.connect()

gecko.call(gecko.getSymbol("coreinit.rpl", "OSShutdown"), 1)

gecko.disconnect()

print("Done.")