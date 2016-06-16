from tcpgecko import TCPGecko
from binascii import hexlify, unhexlify
import sys
try: import __builtin__
except: import builtins as __builtin__

def hex(value, fill):
    return "0x" + __builtin__.hex(value).lstrip("0x").rstrip("L").zfill(fill).upper()

tcp = TCPGecko("192.168.0.10")
title_id = 0x0005000010144F00 #Smash USA
SYSCheckTitleExists = tcp.get_symbol("sysapp.rpl", "SYSCheckTitleExists", True)
doesExist = SYSCheckTitleExists(title_id >> 32, title_id & 0xFFFFFFFF)
if not doesExist: print("Title " + hex(title_id, 16) + " does not exist!")
else:
    SYSLaunchTitle = tcp.get_symbol("sysapp.rpl", "SYSLaunchTitle", True)
    SYSLaunchTitle(title_id >> 32, title_id & 0xFFFFFFFF)
    print("Game switched!")
tcp.s.close()
