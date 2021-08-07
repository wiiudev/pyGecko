import socket, struct, re

class Exception(Exception):
	pass

def onlyCharactersIpAdd(ip):
	check = re.compile(r'[^0-9.]').search
	return not bool(check(ip))

def checkip(ip):
	pieces = ip.split('.')
	if len(pieces) != 4: return False
	try: return all(0<=int(p)<256 for p in pieces)
	except ValueError: return False

class uGecko:
	def __init__(self, ip):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
		if not onlyCharactersIpAdd(ip): raise Exception("The entered IP address is not only composed of numbers and dots.") 
		if not checkip(ip): raise Exception("The entered IP address does not have a valid structure!")
		self.ip = ip
		self.connected:bool = False

	def connect(self, timeout:int = 5)->None:
		if self.ip and self.ip != "" and not self.connected: 
			try:
				self.socket.settimeout(timeout)
				self.socket.connect((str(self.ip), 7331))
				self.socket.settimeout(None)
				self.connected = True
				print("Successfully connected!")
			except: raise Exception(f"Unable to connect to {self.ip}!")
		else: raise Exception("A connection is already in progress!")
			

	def disconnect(self)->None:
		if self.connected:
			self.socket.close() # TODO: Make checks
			self.connected = False
		else: raise Exception("No connection is in progress!")
	
	def isConnected(self)->bool:
		return self.connected

	def validRange(self, address, length)->bool:
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

	def validAccess(self, address:int, length:int, access:str)->bool:
		if   0x01000000 <= address and address + length <= 0x01800000:
			if access.lower() == "read" : return True
			if access.lower() == "write": return False
		elif 0x0E000000 <= address and address + length <= 0x10000000:
			if access.lower() == "read" : return True
			if access.lower() == "write": return False
		elif 0x10000000 <= address and address + length <= 0x50000000:
			if access.lower() == "read" : return True
			if access.lower() == "write": return True
		elif 0xE0000000 <= address and address + length <= 0xE4000000:
			if access.lower() == "read" : return True
			if access.lower() == "write": return False
		elif 0xE8000000 <= address and address + length <= 0xEA000000:
			if access.lower() == "read" : return True
			if access.lower() == "write": return False
		elif 0xF4000000 <= address and address + length <= 0xF6000000:
			if access.lower() == "read" : return True
			if access.lower() == "write": return False
		elif 0xF6000000 <= address and address + length <= 0xF6800000:
			if access.lower() == "read" : return True
			if access.lower() == "write": return False
		elif 0xF8000000 <= address and address + length <= 0xFB000000:
			if access.lower() == "read" : return True
			if access.lower() == "write": return False
		elif 0xFB000000 <= address and address + length <= 0xFB800000:
			if access.lower() == "read" : return True
			if access.lower() == "write": return False
		elif 0xFFFE0000 <= address and address + length <= 0xFFFFFFFF:
			if access.lower() == "read" : return True
			if access.lower() == "write": return True
		else: return False

	def isValidMemoryArea(self, address:int, length:int, skip_verification:bool, type:str = "write")->bool:
		if self.connected:
			if not skip_verification: return self.validRange(address, length) and self.validAccess(address, length, type)
			return True
		else: raise Exception("No connection is in progress!")

	def poke8(self, address:int, value:int, skip:bool = False)->None:
		if self.isValidMemoryArea(address, 1, skip):
			self.socket.send(b'\x01')
			req = struct.pack(">II", address, value)
			self.socket.send(req)
		else: raise Exception("Invalid ram address!")

	def poke16(self, address:int, value:int, skip:bool = False)->None:
		if self.isValidMemoryArea(address, 2, skip):
			self.socket.send(b'\x02')
			req = struct.pack(">II", address, value)
			self.socket.send(req)
		else: raise Exception("Invalid ram address!")

	def poke32(self, address:int, value:int, skip:bool = False)->None:
		if self.isValidMemoryArea(address, 4, skip):
			self.socket.send(b'\x03')
			req = struct.pack(">II", address, value)
			self.socket.send(req)
		else: raise Exception("Invalid ram address!")

	def serialPoke(self, addressTable:list, value:int, skip:bool = False)->None:
		for address in addressTable:
			if type(address)==int: self.poke32(address, value,skip)

	def writeString(self, address:int, string:str, skip:bool = False)->None:
		if self.connected:
			if type(string) != bytes: string = bytes(string, "UTF-8") #Sanitize
			if len(string) % 4: string += bytes((4 - (len(string) % 4)) * b"\x00")
			pos = 0
			for x in range(int(len(string) / 4)):
				self.poke32(address, struct.unpack(">I", string[pos:pos + 4])[0], skip)
				address += 4;pos += 4
		else: raise Exception("No connection is in progress!")

	def clearString(self, startAddress:int, endAddress:int, skip:bool = False)->None:
		if self.connected:
			length = endAddress - startAddress
			i = 0
			while i <= length:
				self.poke32(startAddress + i, 0x00000000, skip)
				i += 4
		else: raise Exception("No connection is in progress!")

	def readString(self, address:int, length:int, decoding:str = "UTF-8", skip:bool = False)->str:
		if self.connected:
			string = self.read(address, length, skip)
			return string.decode(decoding)
		else: raise Exception("No connection is in progress!")

	def read(self, address:int, length:int, skip:bool = False)->bytearray:
		if self.isValidMemoryArea(address, length, skip, "read"):
			if length == 0: raise Exception("Reading memory requires a length!")
			ret = b''
			if length > 0x400:
				for i in range(int(length / 0x400)):
					ret += self.__read(address, 0x400)
					address += 0x400;length -= 0x400
				if length != 0:
					ret += self.__read(address, length)
			else:
				ret = self.__read(address, length)
			return ret
		else: raise Exception("Invalid ram address!")

	def __read(self,address:int,length:int)->bytearray:
		self.socket.send(b'\x04')
		req = struct.pack(">II", int(address), int(address + length))
		self.socket.send(req)
		status = self.socket.recv(1)
		if status == b'\xbd': ret = self.socket.recv(length)
		elif status == b'\xb0': ret = b'\x00' * length
		else: raise Exception("Something went terribly wrong")
		return ret

	def kernelWrite(self, address:int, value:int, skip:bool = False)->None:
		if self.isValidMemoryArea(address, 4, skip):
			self.socket.send(b'\x0B')
			req = struct.pack(">II", int(address), int(value))
			self.socket.send(req)
		else: raise Exception("Invalid ram address!")

	def kernelRead(self, address:int, skip:bool = False)->int:
		if self.isValidMemoryArea(address, 4, skip, "read"):
			self.socket.send(b'\x0C')
			req = struct.pack(">I", int(address))
			self.socket.send(req)
			return struct.unpack(">I", self.socket.recv(4))[0]
		else: raise Exception("Invalid ram address!")

	def getServerStatus(self)->int:
		if self.connected:
			self.socket.send(b'\x50')
			return int.from_bytes(self.socket.recv(1), "big")
		else: raise Exception("No connection is in progress!")

	def isConsolePaused(self)->bool:
		if self.connected:
			self.socket.send(b'\x84')
			return int.from_bytes(self.socket.recv(1), "big")
		else: raise Exception("No connection is in progress!")

	def pauseConsole(self)->None:
		if self.connected: self.socket.send(b'\x82')
		else: raise Exception("No connection is in progress!")

	def resumeConsole(self)->None:
		if self.connected: self.socket.send(b'\x83')
		else: raise Exception("No connection is in progress!")

	def getServerVersion(self)->str:
		if self.connected:
			self.socket.send(b'\x99')
			return self.socket.recv(16).decode("UTF-8").replace('\n', '')
		else: raise Exception("No connection is in progress!")

	def getOsVersion(self)->int:
		if self.connected:
			self.socket.send(b'\x9A')
			return int.from_bytes(self.socket.recv(4), "big")
		else: raise Exception("No connection is in progress!")

	def getVersionHash(self)->int:
		if self.connected:
			self.socket.send(b'\xE0')
			return int.from_bytes(self.socket.recv(4), "big")
		else: raise Exception("No connection is in progress!")

	def getAccountID(self)->str:
		if self.connected:
			self.socket.send(b'\x57')
			return hex(int.from_bytes(self.socket.recv(4), "big")).replace("0x", "")
		else: raise Exception("No connection is in progress!")

	def getCodeHandlerAddress(self)->int:
		if self.connected:
			self.socket.send(b'\x55')
			return int.from_bytes(self.socket.recv(4), "big")
		else: raise Exception("No connection is in progress!")

	def getDataBufferSize(self)->int:
		if self.connected:
			self.socket.send(b'\x51')
			return int.from_bytes(self.socket.recv(4), "big")
		else: raise Exception("No connection is in progress!")

	def getTitleID(self)->int:
		return self.call(self.getSymbol("coreinit.rpl", "OSGetTitleID"))
	
	def getSystemInfo(self)->int:
		ptr:int = self.call(self.getSymbol("coreinit.rpl", "OSGetSystemInfo"),recv=4)
		return ptr

	def search(self, startAddress:int, value:int, length:int)->int:
		if self.connected:
			self.socket.send(b'\x72')
			req = struct.pack(">III", startAddress, value, length)
			self.socket.send(req)
			return int.from_bytes(self.socket.recv(4), "big")
		else: raise Exception("No connection is in progress!")

	def advancedSearch(self, start:int, length:int, value:int, kernel:int, limit:int, aligned:int = 1)->list:
		if self.connected:
			self.socket.send(b'\x73')
			req_val = struct.pack(">I", int(value))
			search_byte_count = len(req_val)
			req = struct.pack(">IIIIII", int(start), int(length), int(kernel), int(limit), int(aligned), int(search_byte_count))
			self.socket.send(req)
			self.socket.send(req_val)
			count = int.from_bytes(self.socket.recv(4), "big") / 4
			foundOffset = []
			for i in range(int(count)):
				foundOffset.append(int.from_bytes(self.socket.recv(4), "big"))
			return foundOffset
		else: raise Exception("No connection is in progress!")

	def getSymbol(self, rplname:str, sysname:str, data = 0)->int:
		if self.connected:
			self.socket.send(b'\x71')
			req = struct.pack('>II', 8, 8 + len(rplname) + 1)
			req += rplname.encode("UTF-8") + b"\x00"
			req += sysname.encode("UTF-8") + b"\x00"
			size = struct.pack(">B", len(req))
			data = struct.pack(">B", data)
			self.socket.send(size)
			self.socket.send(req)
			self.socket.send(data)
			return self.socket.recv(4)
		else: raise Exception("No connection is in progress!")

	def call(self, address:int, *args, recv:int = 8):
		if self.connected:
			arguments = list(args)
			if len(arguments) <= 8:
				while len(arguments) != 8:
					arguments.append(0)
				address = struct.unpack(">I", address)[0]
				req = struct.pack(">I8I", address, *arguments)
				self.socket.send(b'\x70')
				self.socket.send(req)
				if recv == 4: return struct.unpack('>I', self.socket.recv(4))[0]
				return struct.unpack('>Q', self.socket.recv(8))[0]
			else:
				raise Exception("Too many arguments!")
		else: raise Exception("No connection is in progress!")

	def getEntryPointAddress(self)->int:
		if self.connected:
			self.socket.send(b'\xB1')
			return int.from_bytes(self.socket.recv(4), "big")
		else: raise Exception("No connection is in progress!")

	def runKernelCopyService(self)->None:
		if self.connected: self.socket.send(b'\xCD')
		else: raise Exception("No connection is in progress!")

	def clearAssembly(self)->None:
		if self.connected: self.socket.send(b'\xE2')
		else: raise Exception("No connection is in progress!")

	def excecuteAssembly(self, assembly:str)->None:
		if self.connected:
			self.socket.send(b'\x81')
			req = assembly.encode('UTF-8')
			self.socket.send(req)
		else: raise Exception("No connection is in progress!")

	def persistAssembly(self, assembly:str)->None:
		if self.connected:
			self.socket.send(b'\xE1')
			req = assembly.encode('UTF-8')
			self.socket.send(req)
		else: raise Exception("No connection is in progress!")

	def upload(self, startAddress: int, data: bytes) -> None:
		if self.connected:
			self.socket.send(b'\x41')
			req = struct.pack(">II",startAddress,startAddress+len(data))
			self.socket.send(req) # first let the sever know the length
			self.socket.send(data)# then send the data
		else: raise Exception("No connection is in progress!")

	def dump(self, startAddress: int, endAddress: int, skip:bool = False) -> bytearray:
		return self.read(startAddress, endAddress - startAddress, skip)

	def allocateSystemMemory(self, size: int) -> int:
		return self.call(self.getSymbol('coreinit.rpl', 'OSAllocFromSystem'), size, 4, recv = 4)

	def freeSystemMemory(self, address):
		return self.function("coreinit.rpl", "OSFreeToSystem", address)