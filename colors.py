#You're probably better off using the GUI version, but...
#https://gbatemp.net/threads/splatoon-colorizer.406463/
from tcpgecko import TCPGecko
from textwrap import wrap
from struct   import pack
from binascii import unhexlify
import sys

tcp = TCPGecko("192.168.0.8") #Wii U IP address
Colors = b""
for i in range(1, 4): #Ignores Alpha since it doesn't use it
    Color = wrap(sys.argv[i], 2) #Split it into 2 character chunks
    for j in range(3): #Create the RGB floats
        Colors += pack(">f", ord(unhexlify(Color[j])) / 256)
    Colors += pack(">f", 1.0) #Alpha
tcp.writestr(0x12D1E178, Colors) #Only overwrites currently loaded color
                                 #Run a command right after the lobby is "ready"
tcp.s.close()
print("Done!")
