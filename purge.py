from tcpgecko import TCPGecko
#Script to purge Miiverse save cache in Splatoon
tcp = TCPGecko("192.168.137.3")
tcp.writestr(0x12CE0100, b"\x00" * 0x1850) #Only for 2.0.0-2.1.0 AFAIK
tcp.s.close()
print("Done!")
