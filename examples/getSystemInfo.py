from uGecko import uGecko

gecko = uGecko("192.168.1.102")
gecko.connect()

info = gecko.getSystemInfo()
print(f"""
busClockSpeed\t:{info["busClockSpeed"]}
coreClockSpeed\t: {info["coreClockSpeed"]}
timeBase\t: {info["timeBase"]}
L2Size\t: {info["L2Size"]}
cpuRatio\t: {info["cpuRatio"]}""")

gecko.disconnect()

print("Done.")