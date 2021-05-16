import socket, struct

class uGecko:
	def __init__(self, ip):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
		self.ip = ip # TODO: Make checks
		self.connected = False

	def connect(self):
		if self.ip == None or self.ip == "":
			raise BaseException("No ip address has been entered!")
		else:
			try:
				self.socket.connect((str(self.ip), 7331))
				self.connected = True
			except:
				raise BaseException(f"Unable to connect to {self.ip}!")
		

	def disconnect(self):
		self.socket.close() # TODO: Make checks
		self.connected = False

	def isConnected(self):
		return self.connected

	def validRange(self, address, length):
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

	def validAccess(self, address, length, access):
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

	def poke8(self, address, value, skip = False):
		if not skip:
			if not self.validRange(address, 1): raise BaseException("Address range not valid")
			if not self.validAccess(address, 1, "write"): raise BaseException("Cannot write to address")
		self.socket.send(b'\x01')
		req = struct.pack(">II", int(address), int(value))
		self.socket.send(req)
		return

	def poke16(self, address, value, skip = False):
		if not skip:
			if not self.validRange(address, 2): raise BaseException("Address range not valid")
			if not self.validAccess(address, 2, "write"): raise BaseException("Cannot write to address")
		self.socket.send(b'\x02')
		req = struct.pack(">II", int(address), int(value))
		self.socket.send(req)
		return

	def poke32(self, address, value, skip = False):
		if not skip:
			if not self.validRange(address, 4): raise BaseException("Address range not valid")
			if not self.validAccess(address, 4, "write"): raise BaseException("Cannot write to address")
		self.socket.send(b'\x03')
		req = struct.pack(">II", int(address), int(value))
		self.socket.send(req)
		return

	def serialPoke(self, addressTable, value, skip = False):
		if isinstance(addressTable, list):
			for address in addressTable:
				if not skip:
					if not self.validRange(address, 4): raise BaseException("Address range not valid")
					if not self.validAccess(address, 4, "write"): raise BaseException("Cannot write to address")
				self.socket.send(b"\x03")
				req = struct.pack(">II", address, value)
				self.socket.send(req)
			return
		else:
			raise BaseException("Address is not a list!")

	def writeString(self, address, string, skip = False):
		if not skip:
			if not self.validRange(address, len(string)): raise BaseException("Address range not valid")
			if not self.validAccess(address, len(string), "write"): raise BaseException("Cannot write to address")
		if type(string) != bytes: string = bytes(string, "UTF-8") #Sanitize
		if len(string) % 4: string += bytes((4 - (len(string) % 4)) * b"\x00")
		pos = 0
		for x in range(int(len(string) / 4)):
			self.poke32(address, struct.unpack(">I", string[pos:pos + 4])[0])
			address += 4;pos += 4
		return

	def read(self, address, length, skip = False):
		if not skip:
			if length == 0: raise BaseException("Reading memory requires a length!")
			if not self.validRange(address, length): raise BaseException("Address range not valid")
			if not self.validAccess(address, length, "read"): raise BaseException("Cannot read to address")
		ret = b''
		if length > 0x400:
			for i in range(int(length / 0x400)):
				self.socket.send(b'\x04')
				req = struct.pack(">II", int(address), int(address + 0x400))
				self.socket.send(req)
				if status == b'\xbd': ret += self.socket.recv(length)
				elif status == b'\xb0': ret += b'\x00' * length
				else: raise BaseException("Something went terribly wrong")
				address += 0x400;length -= 0x400
			if length != 0:
				self.socket.send(b'\x04')
				req = struct.pack(">II", int(address), int(address + length))
				self.socket.send(req)
				status = self.socket.recv(1)
				if status == b'\xbd': ret += self.socket.recv(length)
				elif status == b'\xb0': ret += b'\x00' * length
				else: raise BaseException("Something went terribly wrong")
		else:
			self.socket.send(b'\x04')
			req = struct.pack(">II", int(address), int(address + length))
			self.socket.send(req)
			status = self.socket.recv(1)
			if status == b'\xbd': ret += self.socket.recv(length)
			elif status == b'\xb0': ret += b'\x00' * length
			else: raise BaseException("Something went terribly wrong")
		return ret

	def kernelWrite(self, address, value, skip = False):
		if not skip:
			if not self.validRange(address, 4): raise BaseException("Address range not valid")
			if not self.validAccess(address, 4, "write"): raise BaseException("Cannot write to address")
		self.socket.send(b'\x0B')
		req = struct.pack(">II", int(address), int(value))
		self.socket.send(req)
		return

	def kernelRead(self, address, skip = False):
		if not skip:
			if not self.validRange(address, 4): raise BaseException("Address range not valid")
			if not self.validAccess(address, 4, "read"): raise BaseException("Cannot read to address")
		self.socket.send(b'\x0C')
		req = struct.pack(">I", int(address))
		self.socket.send(req)
		return struct.unpack(">I", self.socket.recv(4))[0]

	def getServerStatus(self):
		self.socket.send(b'\x50')
		return int.from_bytes(self.socket.recv(1), "big")

	def isConsolePaused(self):
		self.socket.send(b'\x84')
		val = int.from_bytes(self.socket.recv(1), "big")
		if val == 1:
			return True
		else:
			return False

	def pauseConsole(self):
		self.socket.send(b'\x82')

	def resumeConsole(self):
		self.socket.send(b'\x83')

	def getServerVersion(self):
		self.socket.send(b'\x99')
		return self.socket.recv(16).decode("UTF-8").replace('\n', '')

	def getOsVersion(self):
		self.socket.send(b'\x9A')
		return int.from_bytes(self.socket.recv(4), "big")

	def getVersionHash(self):
		self.socket.send(b'\xE0')
		return int.from_bytes(self.socket.recv(4), "big")

	def getAccountID(self):
		self.socket.send(b'\x57')
		return hex(int.from_bytes(self.socket.recv(4), "big")).replace("0x", "")

	def getCoreHandlerAddress(self):
		self.socket.send(b'\x55')
		return hex(int.from_bytes(self.socket.recv(4), "big"))

	def getDataBufferSize(self):
		self.socket.send(b'\x51')
		return int.from_bytes(self.socket.recv(4), "big")

	def search(self, startAddress, value, length):
		self.socket.send(b'\x72')
		req = struct.pack(">III", int(startAddress), int(value), int(length))
		self.socket.send(req)
		return hex(int.from_bytes(self.socket.recv(4), "big"))

	def advancedSearch(self, start, length, value, kernel, limit, aligned):
		self.socket.send(b'\x73')
		req_val = struct.pack(">I", int(value))
		search_byte_count = len(req_val)
		req = struct.pack(">IIIIII", int(start), int(length), int(kernel), int(limit), int(aligned), int(search_byte_count))
		self.socket.send(req)
		self.socket.send(req_val)
		count = int.from_bytes(self.socket.recv(4), "big") / 4
		foundOffset = []
		for i in range(int(count)):
			foundOffset.append(hex(int.from_bytes(self.socket.recv(4), "big")))
		return foundOffset

	def getSymbol(self, rplname, sysname, data = 0):
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

	def call(self, address, *args):
		arguments = list(args)
		if len(arguments) <= 8:
			while len(arguments) != 8:
				arguments.append(0)
			address = struct.unpack(">I", address)[0]
			req = struct.pack(">I8I", address, *arguments)
			self.socket.send(b'\x70')
			self.socket.send(req)
			return struct.unpack('>I', self.socket.recv(8)[:4])[0]
		else:
			raise BaseException("Too many arguments!")

	def getEntryPointAddress(self):
		self.socket.send(b'\xB1')
		return hex(int.from_bytes(self.socket.recv(4), "big"))

	def runKernelCopyService(self):
		self.socket.send(b'\xCD')
		return

	def clearAssembly(self):
		self.socket.send(b'\xE2')
		return

	def excecuteAssembly(self, assembly):
		self.socket.send(b'\x81')
		req = assembly.encode('UTF-8')
		self.socket.send(req)

	def persistAssembly(self, assembly):
		self.socket.send(b'\xE1')
		req = assembly.encode('UTF-8')
		self.socket.send(req)