from tcpgecko import TCPGecko
from textwrap import wrap
from struct   import pack
from binascii import hexlify, unhexlify
import sys

def pokecolor(pos, string):
    color = textwrap.wrap(string, 4)
    tcp.pokemem(pos, struct.unpack(">I", color[0])[0])
    tcp.pokemem(pos + 4, struct.unpack(">I", color[1])[0])
    tcp.pokemem(pos + 8, struct.unpack(">I", color[2])[0])
    tcp.pokemem(pos + 12, struct.unpack(">I", color[3])[0])

tcp = TCPGecko("192.168.137.3")
Colors = b""
for i in range(1, 4): #Ignores Alpha since it doesn't use it
    Color = wrap(sys.argv[i], 2) #Split it into 2 character chunks
    for j in range(3):
        Colors += pack(">f", ord(unhexlify(Color[j])) / 256)
    Colors += pack(">f", 1.0)
tcp.writestr(0x12D14F64, Colors) #Only overwrites currently loaded color
                                 #You need to figure out timing to apply
tcp.s.close()
print("Done.")
