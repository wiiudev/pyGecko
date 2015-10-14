from tcpgecko import TCPGecko
import sys
sys.argv.append("210")
#Codename Octohax
tcp = TCPGecko("192.168.137.3")
if sys.argv[1] == "100": #For 1.0.0-?
    tcp.writestr(0x105068F0, b"Tnk_Rvl00")
    tcp.writestr(0x1051A500, b"Tnk_Rvl00")
    tcp.writestr(0x105DBFE0, b"Rival00")
    tcp.writestr(0x105DBFEC, b"Rival00_Hlf")
    tcp.writestr(0x105DBFFC, b"Rival_Squid")
    #tcp.pokemem(0x12CB05A0, 42069)
elif sys.argv[1] == "130": #for 1.3.0
    tcp.writestr(0x105068F0, b"Tnk_Rvl00")
    tcp.writestr(0x105D4000, b"Tnk_Rvl00")
    tcp.writestr(0x105DC118, b"Rival00")
    tcp.writestr(0x105DC124, b"Rival00_Hlf")
    tcp.writestr(0x105DC134, b"Rival_Squid")
    #tcp.pokemem(0x12CB07A0, 42069)
elif sys.argv[1] == "200": #For 2.0.0
    tcp.writestr(0x10506AB0, b"Tnk_Rvl00")
    tcp.writestr(0x105E0278, b"Tnk_Rvl00")
    tcp.writestr(0x105E85B0, b"Rival00")
    tcp.writestr(0x105E85BC, b"Rival00_Hlf")
    tcp.writestr(0x105E85CC, b"Rival_Squid")
    tcp.writestr(0x12BE2350, b"Tnk_Rvl00")
    tcp.writestr(0x12BE239C, b"Tnk_Rvl00")
    tcp.writestr(0x12BE23E8, b"Tnk_Rvl00")
elif sys.argv[1] == "210": #For 2.1.0
    tcp.writestr(0x10506AF8, b"Tnk_Rvl00")
    tcp.writestr(0x105E0350, b"Tnk_Rvl00")
    tcp.writestr(0x105E8698, b"Rival00")
    tcp.writestr(0x105E86A4, b"Rival00_Hlf")
    tcp.writestr(0x105E86B4, b"Rival_Squid")
    tcp.writestr(0x12BE2350, b"Tnk_Rvl00")
    tcp.writestr(0x12BE239C, b"Tnk_Rvl00")
    tcp.writestr(0x12BE23E8, b"Tnk_Rvl00")
    tcp.pokemem(0x12CC7C80, 0x00000000) #Enforce Female Inkling
tcp.s.close()
print("Done.")
