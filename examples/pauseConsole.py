import time
from ugecko import uGecko

gecko = uGecko("192.168.1.57")
gecko.connect()

gecko.pauseConsole()
print(f"Console Paused: {str(gecko.isConsolePaused())}")
time.sleep(5)
gecko.resumeConsole()
print(f"Console Paused: {str(gecko.isConsolePaused())}")

gecko.disconnect()

print("Done.")