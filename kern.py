from tcpgecko import TCPGecko
import sys

tcp = TCPGecko("192.168.1.82")
print(tcp.readkern(0x10000000))
tcp.s.close()
print("Done.")
