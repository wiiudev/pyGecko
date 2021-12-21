import socket, struct
from typing import Union

from .enums.Commands import Commands

from .utils.Errors import *
from .utils.Memory import Memory
from .utils.Verification import IP_Verification

class uGecko:
    """Python library for use with TCPGecko. Requires kernel exploit to use."""

    def __init__(self, ip: str, port: int = 7331, debug_mode: bool = False) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        if not IP_Verification(ip): raise InvalidIpAddressException("The IP address given is not valid!")
        self.__ip = ip
        self.__port = port
        self.__connected = False
        self.__debug_mode = debug_mode

    def setDebugMode(self, debug_mode: bool) -> None:
        self.__debug_mode = debug_mode

    def getDebugMode(self) -> bool:
        return self.__debug_mode

    def connect(self, timeout: int = 5) -> None:
        if self.__ip and self.__ip != "":
            if not self.__connected:
                try:
                    if self.__debug_mode: print(f"Connecting to {self.__ip}:{self.__port}...")
                    self.__socket.settimeout(timeout)
                    self.__socket.connect((str(self.__ip), int(self.__port)))
                    self.__connected = True
                    if self.__debug_mode: print("Connected!")
                except: raise ConnectionErrorException(f"Unable to connect to {self.__ip} !") 
            else: raise ConnectionIsAlreadyInProgressException(f"A connection to {self.__ip} is already in progress!")
        else: raise NoIpEnteredException("No IP address has been specified to connect!")

    def disconnect(self):
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.close()
        self.__connected = False

    def isConnected(self) -> bool:
        return self.__connected

    def getWiiuIp(self) -> str:
        return f"{str(self.__ip)}:{str(self.__port)}" if self.__ip else -1

    def poke8(self, address: int, value: int, skip_verification: bool = False) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        if not Memory.isValidMemoryArea(address, 1, skip_verification): raise InvalidMemoryAreaException("The address given is not valid!")

        self.__socket.send(Commands.POKE_8.value)
        self.__socket.send(struct.pack(">II", address, value))

    def poke16(self, address: int, value: int, skip_verification: bool = False) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        if not Memory.isValidMemoryArea(address, 4, skip_verification): raise InvalidMemoryAreaException("The address given is not valid!")

        self.__socket.send(Commands.POKE_16.value)
        self.__socket.send(struct.pack(">II", address, value))

    def poke32(self, address: int, value: int, skip_verification: bool = False) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        if not Memory.isValidMemoryArea(address, 8, skip_verification): raise InvalidMemoryAreaException("The address given is not valid!")

        self.__socket.send(Commands.POKE_32.value)
        self.__socket.send(struct.pack(">II", address, value))

    def seriaPoke(self, address_list: Union[list, tuple], value: int, skip_verification: bool = False) -> None:
        for address in address_list:
            self.poke32(address, value, skip_verification)

    def writeString(self, address: int, string: Union[str, bytes], skip_verification: bool = False):
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")

        if type(string) != bytes: string = bytes(string, "UTF-8")
        if len(string) % 4: string += b"\x00" * (4 - len(string) % 4)
        position = 0
        for i in range(int(len(string) / 4)):
            self.poke32(address + position, struct.unpack(">I", string[position:position + 4])[0], skip_verification)
            position += 4

    def clearString(self, start_address: int, end_address: int, skip_verification: bool = False) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")

        length = end_address - start_address ; position = 0
        while position <= length:
            self.poke32(start_address + position, 0x00000000, skip_verification)
            position += 4

    def readString(self, address: int, length: int, charset: str = "UTF-8", skip_verification: bool = False) -> str:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        
        string = self.read(address, length, skip_verification)
        return string.decode(charset)

    def read(self, address: int, length: int = 4, skip_verification: bool = False) -> bytearray:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        if not Memory.isValidMemoryArea(address, length, skip_verification, "read"): raise InvalidMemoryAreaException("The address given is not valid!")

        if length == 0: raise InvalidLengthException("The length given is not valid!")
        ret = b''

        if length > 0x400:
            for i in range(int(length / 0x400)):
                ret += self.__read(address + i * 0x400, 0x400)
                address += 0x400 ; length -= 0x400
            
            if length != 0:
                ret += self.__read(address, length)
        else:
            ret = self.__read(address, length)

        return ret

    def __read(self, address: int, length: int) -> bytearray:
        self.__socket.send(Commands.READ_MEMORY.value)
        self.__socket.send(struct.pack(">II", address, address + length))

        status = self.__socket.recv(1)
        if status == b'\xbd':
            ret = self.__socket.recv(length)
        elif status == b'\xb0':
            ret = b'\x00' * length
        else:
            raise ReadMemoryException("Unable to read memory!")
        
        return ret

    def kernelWrite(self, address: int, value: int, skip_verification: bool = False) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        if not Memory.isValidMemoryArea(address, 4, skip_verification): raise InvalidMemoryAreaException("The address given is not valid!")

        self.__socket.send(Commands.KERNEL_WRITE.value)
        self.__socket.send(struct.pack(">II", address, value))

    def kernelRead(self, address: int, skip_verification: bool = False) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        if not Memory.isValidMemoryArea(address, 4, skip_verification, "read"): raise InvalidMemoryAreaException("The address given is not valid!")

        self.__socket.send(Commands.KERNEL_READ.value)
        self.__socket.send(struct.pack(">I", address))

        return int.from_bytes(self.__socket.recv(4), byteorder="big")

    def getServerStatus(self) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.SERVER_STATUS.value)
        return int.from_bytes(self.__socket.recv(1), byteorder="big")

    def isConsolePaused(self) -> bool:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.IS_CONSOLE_PAUSED.value)
        return bool(int.from_bytes(self.__socket.recv(1), byteorder="big"))

    def pauseConsole(self) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.PAUSE_CONSOLE.value)

    def resumeConsole(self) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.RESUME_CONSOLE.value)

    def getServerVersion(self) -> str:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.GET_SERVER_VERSION.value)
        return self.__socket.recv(16).decode("UTF-8").replace("\n", "")

    def getOsVersion(self) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.GET_OS_VERSION.value)
        return int.from_bytes(self.__socket.recv(4), byteorder="big")

    def getVersionHash(self) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.GET_VERSION_HASH.value)
        return int.from_bytes(self.__socket.recv(4), byteorder="big")

    def getAccountID(self) -> str:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.ACCOUNT_IDENTIFIER.value)
        return hex(int.from_bytes(self.__socket.recv(4), byteorder="big")).replace("0x", "")

    def getCodeHandlerAddress(self) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.GET_CODE_HANDLER_ADDRESS.value)
        return int.from_bytes(self.__socket.recv(4), byteorder="big")

    def getDataBufferSize(self) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.GET_DATA_BUFFER_SIZE.value)
        return int.from_bytes(self.__socket.recv(4), byteorder="big")

    def getTitleID(self) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        return self.call(self.getSymbol("coreinit.rpl", "OSGetTitleID"), recv = 8)

    def getSystemInformation(self) -> dict:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")

        ptr:int = self.call(self.getSymbol("coreinit.rpl", "OSGetSystemInfo"))
        data = struct.unpack(">IIIIIII", self.read(ptr, 0x1c))

        sysInformation = dict()
        sysInformation["busClockSpeed"] = data[0]
        sysInformation["coreClockSpeed"] = data[1]
        sysInformation["timeBase"] = data[2]
        sysInformation["L2Size"] = [data[3], data[4], data[5]]
        sysInformation["cpuRatio"] = data[6]

        return sysInformation

    def getSymbol(self, rpl_name: str, symbol_name: str, data = 0) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")

        self.__socket.send(Commands.GET_SYMBOL.value)
        
        req = struct.pack(">II", 8, 8 + len(rpl_name) + 1)
        req += rpl_name.encode("UTF-8") + b'\x00'
        req += symbol_name.encode("UTF-8") + b'\x00'
        
        size = struct.pack(">B", len(req))
        data = struct.pack(">B", data)

        self.__socket.send(size)
        self.__socket.send(req)
        self.__socket.send(data)

        return struct.unpack(">I", self.__socket.recv(4))[0]

    def call(self, address: int, *args, recv: int = 4):
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        
        arguments = list(args)
        if len(arguments) <= 8:
            while len(arguments) != 8:
                arguments.append(0)

            req = struct.pack(">I8I", address, *arguments)
            self.__socket.send(Commands.REMOTE_PROCEDURE_CALL.value)
            self.__socket.send(req)

            return struct.unpack('>Q', self.__socket.recv(8))[0] >> 32 * (recv == 4)
        else: raise TooManyArgumentsException("Too many arguments!")

    def search(self, start_address: int, length: int, value: int, skip_verification: bool = False) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        if not Memory.isValidMemoryArea(start_address, length, skip_verification, "read"): raise InvalidMemoryAreaException("Invalid memory area!")

        self.__socket.send(Commands.MEMORY_SEARCH.value)
        self.__socket.send(struct.pack(">III", start_address, value, length))

        return int.from_bytes(self.__socket.recv(4), byteorder="big")

    def advancedSearch(self, start_address: int, length: int, value: int, kernel: int, limit: int, aligned: int = 1, skip_verification: bool = False) -> list[int]:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        if not Memory.isValidMemoryArea(start_address, length, skip_verification, "read"): raise InvalidMemoryAreaException("Invalid memory area!")

        self.__socket.send(Commands.ADVANCED_MEMORY_SEARCH.value)
        
        req_val = struct.pack(">I", value)
        search_byte_count = len(req_val)

        req = struct.pack(">IIIIII", start_address, length, kernel, limit, aligned, search_byte_count)
        self.__socket.send(req)
        self.__socket.send(req_val)

        count = int.from_bytes(self.__socket.recv(4), byteorder="big") / 4
        foundOffsets = list()
        for i in range(int(count)):
            foundOffsets.append(int.from_bytes(self.__socket.recv(4), byteorder="big"))
        return foundOffsets

    def getEntryPointAddress(self) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        
        self.__socket.send(Commands.GET_ENTRY_POINT_ADDRESS.value)
        return int.from_bytes(self.__socket.recv(4), byteorder="big")

    def runKernelCopyService(self) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.RUN_KERNEL_COPY_SERVICE.value)

    def clearAssembly(self) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.CLEAR_ASSEMBLY.value)

    def executeAssembly(self, assembly: str) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.EXECUTE_ASSEMBLY.value)
        self.__socket.send(assembly.encode("UTF-8"))

    def persistAssembly(self, assembly: str) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.__socket.send(Commands.PERSIST_ASSEMBLY.value)
        self.__socket.send(assembly.encode("UTF-8"))

    def dump(self, start_address: int, end_address: int, skip_verification: bool = False) -> bytearray:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        return self.read(start_address, end_address - start_address, skip_verification)

    def allocateSystemMemory(self, size: int, alignment: int = 4) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        return self.call(self.getSymbol("coreinit.rpl", "OSAllocFromSystem"), size, alignment, recv = 4)

    def freeSystemMemory(self, address: int) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        self.call(self.getSymbol("coreinit.rpl", "OSFreeToSystem"), address)

    def malloc(self, size: int, alignment: int = 4) -> int:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")

        symbol  = self.getSymbol("coreinit.rpl", "MEMAllocFromDefaultHeapEx", 1)
        address = struct.unpack(">I", self.read(symbol, 4))[0]
        return self.call(address, size, alignment)

    def free(self, address: int) -> None:
        if not self.__connected: raise ConnectionIsNotInProgressException("No connection is in progress!")
        
        symbol  = self.getSymbol("coreinit.rpl", "MEMFreeToDefaultHeap", 1)
        addr = struct.unpack(">I", self.read(symbol, 4))[0]
        self.call(addr, address)

    def __upload(self, startAddress: int, data: bytes) -> None:
        self.__socket.send(b'\x41')
        req = struct.pack(">II",startAddress, startAddress+len(data))
        self.__socket.send(req)  # first let the server know the length
        self.__socket.send(data) # then send the data

    def upload(self, startAddress: int, data: bytes, debug_print:bool = False) -> None:
        if self.connected:
            length = len(data)
            maxLength = self.getDataBufferSize()
            if length > maxLength:
                pos = 0
                if debug_print: print(f"length over {hex(maxLength)}\nuploading in blocks!")
                for i in range(int(length/maxLength)):
                    self.__upload(startAddress, data[pos:pos+maxLength])
                    pos += maxLength; length-=maxLength; startAddress+=maxLength
            if length != 0: self.__upload(startAddress, data[pos:pos+length])
            else: self.__upload(startAddress, data)
        else: raise Exception("No connection is in progress!")