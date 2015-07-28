from tcpgecko import TCPGecko

tcp = TCPGecko("192.168.0.8")
tcp.writestr(0x105068F0, "Tnk_Rvl00") #For 1.0.0-?
tcp.writestr(0x1051A500, "Tnk_Rvl00")
tcp.writestr(0x105DBFE0, "Rival00")
tcp.writestr(0x105DBFEC, "Rival00_Hlf")
tcp.writestr(0x105DBFFC, "Rival_Squid")
tcp.pokemem(0x12CB05A0, 42069)
'''tcp.writestr(0x105068F0, "Tnk_Rvl00") #for 1.3.0
tcp.writestr(0x105D4000, "Tnk_Rvl00")
tcp.writestr(0x105DC118, "Rival00")
tcp.writestr(0x105DC124, "Rival00_Hlf")
tcp.writestr(0x105DC134, "Rival_Squid")
tcp.pokemem(0x12CB07A0, 42069)'''
tcp.s.close()
print("Done.")
