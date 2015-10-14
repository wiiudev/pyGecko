import struct

class switch(object): #Taken from http://code.activestate.com/recipes/410692/
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False
'''Example Use Case for switch:
for case in switch(variable):
    if case(0):
        #dostuff
    elif case(1):
        #dostuff
    else: #default
        #dodefaultstuff'''

def hexstr(data, length): #Pad hex to value for prettyprint
    return hex(data).lstrip("0x").rstrip("L").zfill(length).upper()
def hexstr0(data): #Uppercase hex to string
    return "0x" + hex(data).lstrip("0x").rstrip("L").upper()
def binr(byte): #Get bits as a string
    return bin(byte).lstrip("0b").zfill(8)
def uint8(data, pos):
    return struct.unpack(">B", data[pos:pos + 1])[0]
def uint16(data, pos):
    return struct.unpack(">H", data[pos:pos + 2])[0]
def uint24(data, pos):
    return struct.unpack(">I", "\00" + data[pos:pos + 3])[0] #HAX
def uint32(data, pos):
    return struct.unpack(">I", data[pos:pos + 4])[0]

def getstr(data, pos): #Keep incrementing till you hit a stop
    string = ""
    while data[pos] != 0:
        if pos != len(data):
            string += chr(data[pos])
            pos += 1
        else: break
    return string
