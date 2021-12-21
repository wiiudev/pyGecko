from ugecko import uGecko

gecko = uGecko("192.168.1.57")
gecko.connect()

info = gecko.getSystemInformation()
print(f"""
busClockSpeed\t: {info["busClockSpeed"]}
coreClockSpeed\t: {info["coreClockSpeed"]}
timeBase\t: {info["timeBase"]}
L2Size\t: {info["L2Size"]}
cpuRatio\t: {info["cpuRatio"]}""")

gecko.disconnect()

print("Done.")