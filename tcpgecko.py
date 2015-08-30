import socket, struct
from common import *

def enum(**enums):
    return type('Enum', (), enums)
global printe
class TCPGecko:
    def __init__(self, ip):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.s.connect((str(ip), 7331))

    def readmem(self, address, length):
        if length == 0: raise BaseException, "Why are you giving me no length" #Please don't do this to me
        if not self.ValidMemory().validrange(address, length): return
        if not self.ValidMemory().validaccess(address, length, "read"): return
        self.s.send("\x04") #cmd_readmem
        request = struct.pack(">II", address, address + length)
        self.s.send(request)
        status  = self.s.recv(1)
        if status == "\xbd": #Non-zero memory was found
            response = self.s.recv(length)
        elif status == "\xb0": #All zeroes
            response = "\x00" * length
        else: return #Something went terribly wrong
        return response

    def dumpmem(self, address, length, filename="memdump.bin"):
        if length == 0: raise BaseException, "Why are you giving me no length" #Please don't do this to me
        if not self.ValidMemory().validrange(address, length): return
        if not self.ValidMemory().validaccess(address, length, "read"): return
        f = open(filename, "wb")
        for i in range((length+(0x400-(length%0x400)))/0x400):
            if length < 0x400: ret = self.readmem(address, length)
            else: ret = self.readmem(address, 0x400)
            print(hexstr0(address)) #now that we know it's been read
            print(hexstr0(length))
            f.write(ret)
            address += 0x400
            length -= 0x400
        f.close()
        
    def readkern(self, address):
        if not self.ValidMemory().validrange(address, 4): return
        if not self.ValidMemory().validaccess(address, 4, "read"): return
        self.s.send("\x0C") #cmd_readkern
        request = struct.pack(">I", int(address))
        self.s.send(request)
        value  = struct.unpack(">I", self.s.recv(4))[0];
        return value

    def writekern(self, address, value):
        if not self.ValidMemory().validrange(address, 4): return
        if not self.ValidMemory().validaccess(address, 4, "write"): return
        self.s.send("\x0b") #cmd_writekern
        print(value)
        request = struct.pack(">II", int(address), int(value))
        self.s.send(request)
        return

    def pokemem(self, address, value):
        if not self.ValidMemory().validrange(address, 4): return
        if not self.ValidMemory().validaccess(address, 4, "write"): return
        self.s.send("\x03") #cmd_pokemem
        request = struct.pack(">II", int(address), int(value))
        self.s.send(request)
        return

    def writestr(self, address, string):
        if not self.ValidMemory().validrange(address, len(string)): return
        if not self.ValidMemory().validaccess(address, len(string), "write"): return
        if len(string) % 4: string = string.ljust(len(string) + (4 - (len(string) % 4)), "\x00")
        strpos = 0
        for x in range(len(string) / 4):
            self.pokemem(address, int(string[strpos:strpos + 4].encode("hex"), 16))
            address += 4;strpos += 4
        return

    def get_symbol(self, rplname, symname, data=0):
        self.s.send("\x71") #cmd_getsymbol
        request = struct.pack(">II", 8, 8 + len(rplname) + 1)
        request += rplname.encode('utf-8') + b"\x00"
        request += symname.encode('utf-8') + b"\x00"
        length = struct.pack(">I", len(request))
        data = struct.pack(">B", data)
        self.s.send(length)
        self.s.send(request)
        self.s.send(data)
        
        address = self.s.recv(4)
        return ExportedSymbol(address, self, rplname, symname)

    def call(self, address, *args):
        # Turn the arguments into a list and add 0 for unused slots
        arguments = list(args)
        while len(arguments) != 10:
            arguments.append(0)

        self.s.send("\x70") #cmd_rpc
        address = struct.unpack(">I", address)[0]
        request = struct.pack(">I10I", address, *arguments)
        self.s.send(request)

        reply = self.s.recv(8)
        return struct.unpack(">I", reply[:4])[0]

    def function(self, rplname, symname, data=0, *args):
        symbol = self.get_symbol(rplname, symname, data)
        ret = self.call(symbol.address, *args)
        return ret

    def memalign(self, size, pad):
        symbol = ExportedSymbol('\x01\x04\x84\xc0', self, 'coreinit.rpl', 'MEMAllocFromDefaultHeapEx')
        ret = self.call(symbol.address, size, pad)
        return ret

    def freemem(self, data):
        symbol = ExportedSymbol('\x01\x04\x85l', self, "coreinit.rpl", "MEMFreeToDefaultHeap")
        ret = self.call(symbol.address, data)
        return ret

    def OSAlloc(self, size, pad):
        return self.function("coreinit.rpl", "OSAllocFromSystem", 0, size, pad)

    def makeclient(self):
        client = self.memalign(0x1700, 0x20)
        self.function("coreinit.rpl", "FSAddClient", 0, client, 0)
        return client

    def makecmd(self):
        cmdblock = self.memalign(0xA80, 0x20)
        self.function("coreinit.rpl", "FSInitCmdBlock", 0, cmdblock)
        return cmdblock

    def makefsbuf(self):
        buf = self.memalign(0x164, 0x20)
        self.function("coreinit.rpl", "memset", 0, buf, 0x00, 0x180)
        return buf

    def makefilebuf(self):
        buf = self.OSAlloc(0x400, 0x20)
        self.function("coreinit.rpl", "memset", 0, buf, 0x00, 0x400)
        return buf

    def makepath(self, string):
        path = self.OSAlloc(len(string), 0x20)
        size = len(string) + (32 - (len(string) % 32))
        self.function("coreinit.rpl", "memset", 0, path, 0x00, size)
        self.writestr(path, string)
        return path

    def updatepath(self, path, string):
        self.function("coreinit.rpl", "memset", 0, path, 0x00, 0x280)
        self.writestr(path, string)
        return path

    def makeword(self):
        return self.OSAlloc(4, 4)

    def gethandle(self, handle):
        return struct.unpack(">I", self.readmem(handle, 4))[0]

    def makemode(self, mode):
        data = self.makeword()
        self.writestr(data, mode)
        return data

    def FSReadInit(self):
        self.function("coreinit.rpl", "FSInit")
        self.pClient = self.makeclient()
        self.pCmd = self.makecmd()

    def SAVEReadInit(self, slot):
        self.function("nn_save.rpl", "SAVEInit")
        ret = self.function("nn_save.rpl", "SAVEInitSaveDir", 0, slot)
        print(ret)
        self.initsave = True
        self.slot = slot

    def FSOpenDir(self, path):
        if not hasattr(self, "pClient"): self.FSReadInit()
        self.pPath = self.makepath(path)
        self.pDh = self.makeword()
        ret = self.function("coreinit.rpl", "FSOpenDir", 0, self.pClient, self.pCmd, self.pPath, self.pDh, 0xFFFFFFFF)
        self.dh = self.gethandle(self.pDh)
        self.pBuffer = self.makefsbuf()
        return ret

    def SAVEOpenDir(self, path):
        if not hasattr(self, "pClient"): self.FSReadInit()
        if not hasattr(self, "initsave"): self.SAVEReadInit(255) #COMMON
        self.pPath = self.makepath(path)
        ret = self.function("nn_save.rpl", "SAVEOpenDir", 0, self.pClient, self.pCmd, self.slot, self.pPath, self.pDh, 0xFFFFFFFF)
        self.pDh = self.gethandle(self.pDh)
        return ret

    def FSCleanDir(self):
        ret = self.function("coreinit.rpl", "FSCloseDir", 0, self.pClient, self.pCmd, self.dh, 0)
        if ret != 0: raise IOError, "Could not close directory properly"
        self.function("coreinit.rpl", "FSDelClient", 0, self.pClient, 0)
        self.freemem(self.pClient)
        self.freemem(self.pCmd)
        self.freemem(self.pBuffer)
        self.function("coreinit.rpl", "OSFreeToSystem", 0, self.pPath)
        self.function("coreinit.rpl", "OSFreeToSystem", 0, self.pDh)
        
    def FSCleanFile(self):
        ret = self.function("coreinit.rpl", "FSCloseFile", 0, self.pClient, self.pCmd, self.fh, 0)
        self.function("coreinit.rpl", "FSDelClient", 0, self.pClient, 0)
        self.freemem(self.pClient)
        self.freemem(self.pCmd)
        self.freemem(self.pBuffer)
        self.function("coreinit.rpl", "OSFreeToSystem", 0, self.pPath)
        self.function("coreinit.rpl", "OSFreeToSystem", 0, self.mode)
        self.function("coreinit.rpl", "OSFreeToSystem", 0, self.pFh)

    def closeDir(self):
        ret = self.function("coreinit.rpl", "FSCloseDir", 0, self.pClient, self.pCmd, self.pDh, 0xFFFFFFFF)
        return ret

    def getentry(self):
        global printe
        ret = self.function("coreinit.rpl", "FSReadDir", 0, self.pClient, self.pCmd, self.dh, self.pBuffer, 0xFFFFFFFF)
        self.entry = self.readmem(self.pBuffer, 0x164)
        printe = getstr(self.entry, 100) + " "
        self.FileSystem().printflags(uint32(self.entry, 0), self.entry)
        self.FileSystem().printperms(uint32(self.entry, 4))
        print(printe)
        #return ret

    '''def getsave(self, titleid, slot): #For some reason breaks so uncomment one or the other, probs need to exit and reopen app
        #Part 1, scan directory for a file
        if not hasattr(self, "pClient"): self.FSReadInit()
        self.SAVEReadInit(slot)
        self.pPath = self.makepath("")
        self.pDh = self.makeword()
        titleid = struct.unpack(">II", struct.pack(">II", titleid >> 32, titleid & 0xFFFFFFFF)) #There's probably a better way to do this but I'm too tired
        ret = self.function("nn_save.rpl", "SAVEOpenDirOtherApplication", 0, self.pClient, self.pCmd, titleid[0], titleid[1], slot, self.pPath, self.pDh, 0xFFFFFFFF)
        if ret != 0: print(ret);raise IOError, "Could not open save directory"
        self.pBuffer = self.makefsbuf()
        self.dh = self.gethandle(self.pDh)
        if self.getentry() != 0: raise IOError, "Could not find any files in save directory"
        self.FSCleanDir()'''

    def getsave(self, titleid, slot): #For some reason breaks so uncomment one or the other, probs need to exit and reopen app
        #Part 2, read the file
        if not hasattr(self, "pClient"): self.FSReadInit()
        self.SAVEReadInit(slot)
        self.pPath = self.makepath("save.dat")
        self.mode = self.makemode("r")
        self.pFh = self.makeword()
        titleid = struct.unpack(">II", struct.pack(">II", titleid >> 32, titleid & 0xFFFFFFFF)) #There's probably a better way to do this but I'm too tired
        ret = self.function("nn_save.rpl", "SAVEOpenFileOtherApplication", 0, self.pClient, self.pCmd, titleid[0], titleid[1], slot, self.pPath, self.mode, self.pFh, 8) #All but file not found = fatal error
        if ret != 0: raise IOError, "Could not open save file for reading"
        self.pBuffer = self.makefilebuf();print(self.pBuffer)
        if self.pBuffer == 0: raise MemoryError, "Couldn't allocate file buffer"
        self.pFh = self.gethandle(self.pFh);print(self.pFh)
        f = open("save.dat", "wb")
        ret = 1024;pos = 0
        while ret != 0: #read until empty
            ret = self.function("coreinit.rpl", "FSReadFile", 0, self.pClient, self.pCmd, self.pBuffer, 1, ret, self.pFh, 0, 0);print(ret)
            if ret != 0:
                f.write(self.readmem(self.pBuffer, ret))
                pos += ret
        f.close()
        self.function("coreinit.rpl", "FSCloseFile", 0, self.pClient, self.pCmd, self.pFh, 0)
        self.function("coreinit.rpl", "FSDelClient", 0, self.pClient, 0)
        self.freemem(self.pClient)
        self.freemem(self.pCmd)
        self.freemem(self.pBuffer)
        self.function("coreinit.rpl", "OSFreeToSystem", 0, self.pPath)
        self.function("coreinit.rpl", "OSFreeToSystem", 0, self.mode)
        self.function("coreinit.rpl", "OSFreeToSystem", 0, self.pFh)
        print("Success :)")

    class FileSystem:
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
        
    class ValidMemory:
        class AddressRange(object):
            def __init__(self, id, low, high):
                self.id = id
                self.low = low
                self.high = high

        AddressType = enum( #Read, Write, Execute, Hardware
            Rw       = 0x1100, 
            Ro       = 0x1000,
            Ex       = 0x1010,
            Hardware = 0x0001, # ???
            Unknown  = 0x0000)

        AddressRanges = [
            AddressRange(AddressType.Ex, 0x01000000, 0x01800000),
            AddressRange(AddressType.Ex, 0x0e300000, 0x10000000),
            AddressRange(AddressType.Rw,  0x10000000,0x50000000),
            AddressRange(AddressType.Ro,  0xe0000000,0xe4000000),
            AddressRange(AddressType.Ro,  0xe8000000,0xea000000),
            AddressRange(AddressType.Ro,  0xf4000000,0xf6000000),
            AddressRange(AddressType.Ro,  0xf6000000,0xf6800000),
            AddressRange(AddressType.Ro,  0xf8000000,0xfb000000),
            AddressRange(AddressType.Ro,  0xfb000000,0xfb800000),
            AddressRange(AddressType.Rw,  0xfffe0000,0xffffffff)]

        def validrange(self, address, length):
            for addr in self.AddressRanges:
                if address <= addr.low and address < addr.high:
                    if address + length <= addr.high:
                        return True
            return False

        def validaccess(self, address, length, perm):
            for addr in self.AddressRanges:
                if address <= addr.low and address < addr.high:
                    if address + length <= addr.high:
                        if perm.lower() == "read":
                            if addr.id & 0x1000:
                                return True
                        if perm.lower() == "write":
                            if addr.id & 0x0100:
                                return True
            return False

class ExportedSymbol(object): #Copypasta from rpc.py
    def __init__(self, address, rpc=None, rplname=None, symname=None):
        self.address = address
        self.rpc = rpc
        self.rplname = rplname
        self.symname = symname
        print(symname, address)
        
    def __call__(self, *args):
        return self.rpc.call(self.address, *args)
    
def symbol(rplname, symname): #Copypasta from rpc.py
    if not symname in globals():
        globals()[symname] = rpc.get_symbol(rplname, symname)
