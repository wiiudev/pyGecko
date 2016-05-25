import socket, struct
from common import *
from binascii import hexlify, unhexlify

def enum(**enums):
    return type('Enum', (), enums)

class TCPGecko:
    def __init__(self, *args):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        print("Connecting to " + str(args[0]) + ":7331")
        self.s.connect((str(args[0]), 7331)) #IP, 1337 reversed, Cafiine uses 7332+
        print("Connected!")

    def readmem(self, address, length): #Number of bytes
        if length == 0: raise BaseException("Reading memory requires a length (# of bytes)")
        if not self.validrange(address, length): raise BaseException("Address range not valid")
        if not self.validaccess(address, length, "read"): raise BaseException("Cannot read from address")
        ret = b""
        if length > 0x400:
            print("Length is greater than 0x400 bytes, need to read in chunks")
            print("Start address:   " + hexstr0(address))
            for i in range(int(length / 0x400)): #Number of blocks, ignores extra
                self.s.send(b"\x04") #cmd_readmem
                request = struct.pack(">II", address, address + 0x400)
                self.s.send(request)
                status = self.s.recv(1)
                if   status == b"\xbd": ret += self.s.recv(0x400)
                elif status == b"\xb0": ret += b"\x00" * 0x400
                else: raise BaseException("Something went terribly wrong")
                address += 0x400;length -= 0x400
                print("Current address: " + hexstr0(address))
            if length != 0: #Now read the last little bit
                self.s.send(b"\x04")
                request = struct.pack(">II", address, address + length)
                self.s.send(request)
                status = self.s.recv(1)
                if   status == b"\xbd": ret += self.s.recv(length)
                elif status == b"\xb0": ret += b"\x00" * length
                else: raise BaseException("Something went terribly wrong")
            print("Finished!")
        else:
            self.s.send(b"\x04")
            request = struct.pack(">II", address, address + length)
            self.s.send(request)
            status = self.s.recv(1)
            if   status == b"\xbd": ret += self.s.recv(length)
            elif status == b"\xb0": ret += b"\x00" * length
            else: raise BaseException("Something went terribly wrong")
        return ret

    def readkern(self, address): #Only takes 4 bytes, may need to run multiple times
        if not self.validrange(address, 4): raise BaseException("Address range not valid")
        if not self.validaccess(address, 4, "write"): raise BaseException("Cannot write to address")
        self.s.send(b"\x0C") #cmd_readkern
        request = struct.pack(">I", int(address))
        self.s.send(request)
        value  = struct.unpack(">I", self.s.recv(4))[0]
        return value

    def writekern(self, address, value): #Only takes 4 bytes, may need to run multiple times
        if not self.validrange(address, 4): raise BaseException("Address range not valid")
        if not self.validaccess(address, 4, "write"): raise BaseException("Cannot write to address")
        self.s.send(b"\x0B") #cmd_readkern
        print(value)
        request = struct.pack(">II", int(address), int(value))
        self.s.send(request)
        return

    def pokemem(self, address, value): #Only takes 4 bytes, may need to run multiple times
        if not self.validrange(address, 4): raise BaseException("Address range not valid")
        if not self.validaccess(address, 4, "write"): raise BaseException("Cannot write to address")
        self.s.send(b"\x03") #cmd_pokemem
        request = struct.pack(">II", int(address), int(value))
        self.s.send(request) #Done, move on
        return

    def search32(self, address, value, size):
        self.s.send(b"\x72") #cmd_search32
        request = struct.pack(">III", address, value, size)
        self.s.send(request)
        reply = self.s.recv(4)
        return struct.unpack(">I", reply)[0]

    def getversion(self):
        self.s.send(b"\x9A") #cmd_os_version
        reply = self.s.recv(4)
        return struct.unpack(">I", reply)[0]

    def writestr(self, address, string):
        if not self.validrange(address, len(string)): raise BaseException("Address range not valid")
        if not self.validaccess(address, len(string), "write"): raise BaseException("Cannot write to address")
        if type(string) != bytes: string = bytes(string, "UTF-8") #Sanitize
        if len(string) % 4: string += bytes((4 - (len(string) % 4)) * b"\x00")
        pos = 0
        for x in range(int(len(string) / 4)):
            self.pokemem(address, struct.unpack(">I", string[pos:pos + 4])[0])
            address += 4;pos += 4
        return
        
    def memalign(self, size, align):
        symbol = self.get_symbol("coreinit.rpl", "MEMAllocFromDefaultHeapEx", True, 1)
        symbol = struct.unpack(">I", symbol.address)[0]
        address = self.readmem(symbol, 4)
        #print("memalign address: " + hexstr0(struct.unpack(">I", address)[0]))
        ret = self.call(address, size, align)
        return ret

    def freemem(self, address):
        symbol = self.get_symbol("coreinit.rpl", "MEMFreeToDefaultHeap", True, 1)
        symbol = struct.unpack(">I", symbol.address)[0]
        addr = self.readmem(symbol, 4)
        #print("freemem address: " + hexstr0(struct.unpack(">I", addr)[0]))
        self.call(addr, address) #void, no return

    def memalloc(self, size, align, noprint=False):
        return self.function("coreinit.rpl", "OSAllocFromSystem", noprint, 0, size, align)

    def freealloc(self, address):
        return self.function("coreinit.rpl", "OSFreeToSystem", True, 0, address)

    def createpath(self, path):
        if not hasattr(self, "pPath"): self.pPath = self.memalloc(len(path), 0x20, True) #It'll auto-pad
        size = len(path) + (32 - (len(path) % 32))
        self.function("coreinit.rpl", "memset", True, 0, self.pPath, 0x00, size)
        self.writestr(self.pPath, path)
        #print("pPath address: " + hexstr0(self.pPath))

    def createstr(self, string):
        address = self.memalloc(len(string), 0x20, True) #It'll auto-pad
        size = len(string) + (32 - (len(string) % 32))
        self.function("coreinit.rpl", "memset", True, 0, address, 0x00, size)
        self.writestr(address, string)
        print("String address: " + hexstr0(address))
        return address

    def FSInitClient(self):
        self.pClient = self.memalign(0x1700, 0x20)
        self.function("coreinit.rpl", "FSAddClient", True, 0, self.pClient)
        #print("pClient address: " + hexstr0(self.pClient))

    def FSInitCmdBlock(self):
        self.pCmd = self.memalign(0xA80, 0x20)
        self.function("coreinit.rpl", "FSInitCmdBlock", True, 0, self.pCmd)
        #print("pCmd address:    " + hexstr0(self.pCmd))

    def FSOpenDir(self, path="/"):
        print("Initializing...")
        self.function("coreinit.rpl",  "FSInit", True)
        if not hasattr(self, "pClient"): self.FSInitClient()
        if not hasattr(self, "pCmd"):    self.FSInitCmdBlock()
        print("Getting memory ready...")
        self.createpath(path)
        self.pDh   = self.memalloc(4, 4, True)
        #print("pDh address: " + hexstr0(self.pDh))
        print("Calling function...")
        ret = self.function("coreinit.rpl", "FSOpenDir", False, 0, self.pClient, self.pCmd, self.pPath, self.pDh, 0xFFFFFFFF)
        self.pDh = int(hexlify(self.readmem(self.pDh, 4)), 16)
        print("Return value: " + hexstr0(ret))

    def SAVEOpenDir(self, path="/", slot=255):
        print("Initializing...")
        self.function("coreinit.rpl",  "FSInit", True, 0)
        self.function("nn_save.rpl", "SAVEInit", True, 0, slot)
        print("Getting memory ready...")
        if not hasattr(self, "pClient"): self.FSInitClient()
        if not hasattr(self, "pCmd"):    self.FSInitCmdBlock()
        self.createpath(path)
        self.pDh   = self.memalloc(4, 4, True)
        #print("pDh address: " + hexstr0(self.pDh))
        print("Calling function...")
        ret = self.function("nn_save.rpl", "SAVEOpenDir", False, 0, self.pClient, self.pCmd, slot, self.pPath, self.pDh, 0xFFFFFFFF)
        self.pDh = int(hexlify(self.readmem(self.pDh, 4)), 16)
        print("Return value: " + hexstr0(ret))

    def FSReadDir(self):
        global printe
        if not hasattr(self, "pBuffer"): self.pBuffer = self.memalign(0x164, 0x20)
        print("pBuffer address: " + hexstr0(self.pBuffer))
        ret = self.function("coreinit.rpl", "FSReadDir", True, 0, self.pClient, self.pCmd, self.pDh, self.pBuffer, 0xFFFFFFFF)
        self.entry = self.readmem(self.pBuffer, 0x164)
        printe = getstr(self.entry, 100) + " "
        self.FileSystem().printflags(uint32(self.entry, 0), self.entry)
        self.FileSystem().printperms(uint32(self.entry, 4))
        print(printe)
        return self.entry, ret

    def SAVEOpenFile(self, path="/", mode="r", slot=255):
        print("Initializing...")
        self.function("coreinit.rpl",  "FSInit", True)
        self.function("nn_save.rpl", "SAVEInit", slot, True)
        print("Getting memory ready...")
        if not hasattr(self, "pClient"): self.FSInitClient()
        if not hasattr(self, "pCmd"):    self.FSInitCmdBlock()
        self.createpath(path)
        self.pMode = self.createstr(mode)
        self.pFh   = self.memalign(4, 4)
        #print("pFh address: " + hexstr0(self.pFh))
        print("Calling function...")
        print("This function may have errors")
        #ret = self.function("nn_save.rpl", "SAVEOpenFile", self.pClient, self.pCmd, slot, self.pPath, self.pMode, self.pFh, 0xFFFFFFFF)
        #self.pFh = int(self.readmem(self.pFh, 4).encode("hex"), 16)
        #print(ret)

    def FSReadFile(self):
        if not hasattr(self, "pBuffer"): self.pBuffer = self.memalign(0x200, 0x20)
        print("pBuffer address: " + hexstr0(self.pBuffer))
        ret = self.function("coreinit.rpl", "FSReadFile", False, 0, self.pClient, self.pCmd, self.pBuffer, 1, 0x200, self.pFh, 0, 0xFFFFFFFF)
        print(ret)
        return tcp.readmem(self.pBuffer, 0x200)

    def get_symbol(self, rplname, symname, noprint=False, data=0):
        self.s.send(b"\x71") #cmd_getsymbol
        request = struct.pack(">II", 8, 8 + len(rplname) + 1) #Pointers
        request += rplname.encode("UTF-8") + b"\x00"
        request += symname.encode("UTF-8") + b"\x00"
        size = struct.pack(">B", len(request))
        data = struct.pack(">B", data)
        self.s.send(size) #Read this many bytes
        self.s.send(request) #Get this symbol
        self.s.send(data) #Is it data?
        address = self.s.recv(4)
        return ExportedSymbol(address, self, rplname, symname, noprint)

    def call(self, address, *args):
        arguments = list(args)
        if len(arguments)>8 and len(arguments)<=16: #Use the big call function
            while len(arguments) != 16:
                arguments.append(0)
            self.s.send(b"\x80")
            address = struct.unpack(">I", address)[0]
            request = struct.pack(">I16I", address, *arguments)
            self.s.send(request)
            reply = self.s.recv(8)
            return struct.unpack(">I", reply[:4])[0]
        elif len(arguments) <= 8: #Use the normal one that dNet client uses
            while len(arguments) != 8:
                arguments.append(0)
            self.s.send(b"\x70")
            address = struct.unpack(">I", address)[0]
            request = struct.pack(">I8I", address, *arguments)
            self.s.send(request)
            reply = self.s.recv(8)
            return struct.unpack(">I", reply[:4])[0]
        else: raise BaseException("Too many arguments!")

    #Data last, only a few functions need it, noprint for the big FS/SAVE ones above, acts as gateway for data arg
    def function(self, rplname, symname, noprint=False, data=0, *args):
        symbol = self.get_symbol(rplname, symname, noprint, data)
        ret = self.call(symbol.address, *args)
        return ret

    def validrange(self, address, length):
        if   0x01000000 <= address and address + length <= 0x01800000: return True
        elif 0x0E000000 <= address and address + length <= 0x10000000: return True #Depends on game
        elif 0x10000000 <= address and address + length <= 0x50000000: return True #Doesn't quite go to 5
        elif 0xE0000000 <= address and address + length <= 0xE4000000: return True
        elif 0xE8000000 <= address and address + length <= 0xEA000000: return True
        elif 0xF4000000 <= address and address + length <= 0xF6000000: return True
        elif 0xF6000000 <= address and address + length <= 0xF6800000: return True
        elif 0xF8000000 <= address and address + length <= 0xFB000000: return True
        elif 0xFB000000 <= address and address + length <= 0xFB800000: return True
        elif 0xFFFE0000 <= address and address + length <= 0xFFFFFFFF: return True
        else: return False

    def validaccess(self, address, length, access):
        if   0x01000000 <= address and address + length <= 0x01800000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return False
        elif 0x0E000000 <= address and address + length <= 0x10000000: #Depends on game, may be EG 0x0E3
            if access.lower() == "read":  return True
            if access.lower() == "write": return False
        elif 0x10000000 <= address and address + length <= 0x50000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0xE0000000 <= address and address + length <= 0xE4000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return False
        elif 0xE8000000 <= address and address + length <= 0xEA000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return False
        elif 0xF4000000 <= address and address + length <= 0xF6000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return False
        elif 0xF6000000 <= address and address + length <= 0xF6800000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return False
        elif 0xF8000000 <= address and address + length <= 0xFB000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return False
        elif 0xFB000000 <= address and address + length <= 0xFB800000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return False
        elif 0xFFFE0000 <= address and address + length <= 0xFFFFFFFF:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        else: return False
        
    class FileSystem: #TODO: Try to clean this up ????
        Flags = enum(
            IS_DIRECTORY    = 0x80000000,
            IS_QUOTA        = 0x40000000,
            SPRT_QUOTA_SIZE = 0x20000000, #Supports .quota_size field
            SPRT_ENT_ID     = 0x10000000, #Supports .ent_id field
            SPRT_CTIME      = 0x08000000, #Supports .ctime field
            SPRT_MTIME      = 0x04000000, #Supports .mtime field
            SPRT_ATTRIBUTES = 0x02000000, #Supports .attributes field
            SPRT_ALLOC_SIZE = 0x01000000, #Supports .alloc_size field
            IS_RAW_FILE     = 0x00800000, #Entry isn't encrypted
            SPRT_DIR_SIZE   = 0x00100000, #Supports .size field, doesn't apply to files
            UNSUPPORTED_CHR = 0x00080000) #Entry name has an unsupported character
        
        Permissions = enum( #Pretty self explanitory
            OWNER_READ  = 0x00004000,
            OWNER_WRITE = 0x00002000,
            OTHER_READ  = 0x00000400,
            OTHER_WRITE = 0x00000200)

        def printflags(self, flags, data):
            global printe
            if flags & self.Flags.IS_DIRECTORY:    printe += " Directory"
            if flags & self.Flags.IS_QUOTA:        printe += " Quota"
            if flags & self.Flags.SPRT_QUOTA_SIZE: printe += " .quota_size: " + hexstr0(uint32(data, 24))
            if flags & self.Flags.SPRT_ENT_ID:     printe += " .ent_id: " + hexstr0(uint32(data, 32))
            if flags & self.Flags.SPRT_CTIME:      printe += " .ctime: " + hexstr0(uint32(data, 36))
            if flags & self.Flags.SPRT_MTIME:      printe += " .mtime: " + hexstr0(uint32(data, 44))
            if flags & self.Flags.SPRT_ATTRIBUTES: pass #weh
            if flags & self.Flags.SPRT_ALLOC_SIZE: printe += " .alloc_size: " + hexstr0(uint32(data, 20))
            if flags & self.Flags.IS_RAW_FILE:     printe += " Raw (Unencrypted) file"
            if flags & self.Flags.SPRT_DIR_SIZE:   printe += " .dir_size: " + hexstr0(uint64(data, 24))
            if flags & self.Flags.UNSUPPORTED_CHR: printe += " !! UNSUPPORTED CHARACTER IN NAME"

        def printperms(self, perms):
            global printe
            if perms & self.Permissions.OWNER_READ:  printe += " OWNER_READ"
            if perms & self.Permissions.OWNER_WRITE: printe += " OWNER_WRITE"
            if perms & self.Permissions.OTHER_READ:  printe += " OTHER_READ"
            if perms & self.Permissions.OTHER_WRITE: printe += " OTHER_WRITE"
                
def hexstr0(data): #0xFFFFFFFF, uppercase hex string
    return "0x" + hex(data).lstrip("0x").rstrip("L").zfill(8).upper()

class ExportedSymbol(object):
    def __init__(self, address, rpc=None, rplname=None, symname=None, noprint=False):
        self.address = address
        self.rpc     = rpc
        self.rplname = rplname
        self.symname = symname
        if not noprint: #Make command prompt not explode when using FS or SAVE functions
            print(symname + " address: " + hexstr0(struct.unpack(">I", address)[0]))

    def __call__(self, *args):
        return self.rpc.call(self.address, *args) #Pass in arguments, run address
