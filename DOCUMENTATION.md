# Documentation / uGecko
This file is intended to explain and show how to use the functions of ___uGecko___.

| Name 	| Description 	| Example 	| Return |
|:----:	|:-----------:	|:-------:	| :------:
|uGecko| Used to initialize uGecko | `gecko = uGecko("192.168.1.102")` | None
||||
|connect()|Allows you to connect to the WiiU.| `gecko.connect()`| None
|disconnect()|Allows you to disconnect to the WiiU.| `gecko.disconnect()`| None
|isConnected()|Allows to know if a connection is in progress or not.| `gecko.isConnected()`|Boolean
||||
|poke8()|Allows to change the value in the ram|`gecko.poke8(address, 0x00)`| None
|poke16()|Allows to change the value in the ram|`gecko.poke16(address, 0x0000)`| None
|poke32()|Allows to change the value in the ram|`gecko.poke32(address, 0x00000000)`| None
|serialPoke()|Allows to write a specific value on several addresses of the ram.|`gecko.poke32(addressTable, 0x3F800000)`| None
|kernelWrite()| Writes a value to memory with Kernel Privileges | `gecko.kernelWrite(0x10000000, 0x00000000)`| None
||||
|read()| Allows to know what is the value of an address | `gecko.read(address, length)` | Value
|kernelRead()| Reads a value to memory with Kernel Privileges | `gecko.kernelRead(address)`| Value
||||
|writeString()| Allows you to write text in the ram | `gecko.writeString(address, "Hello World!")` | None
|readString() | Allows to read a string in the ram | `gecko.readString(address, length)` | String(UTF-8)
|clearString()| Allows you to delete text written in the ram | `gecko.clearString(startAddress, endAddress)` | None
||||
|isConsolePaused()|Allows to know if the console is paused or not|`gecko.isConsolePaused()`| Boolean
|pauseConsole()| Allows you to pause the console | `gecko.pauseConsole()` | None
|resumeConsole()| Allows you to resume the console  | `gecko.resumeConsole()`| None
||||
|getServerStatus()| Allows to know the status of the server | `gecko.getServerStatus()`| Int (0 or 1)
|getServerVersion()| Get the server version (TCPGecko version) | `gecko.getServerVersion()`|  String
|getOsVersion()| Allows to get the version of the console | `gecko.getOsVersion()`| Int
|getVersionHash()| Allows to get the hash of the version | `gecko.getVersionHash()`| Int
|getAccountID()| Allows you to retrieve the identifier of the account currently connected to the console. | `gecko.getAccountID()`| String
|getCoreHandlerAddress()| Allows you to get the address of the core handler. | `gecko.getCoreHandlerAddress()`| Hex
|getDataBufferSize()| return the Max size of the DataBuffer | `gecko.getDataBufferSize()`| Int
|getTitleID()| returns the current app titleID | `gecko.getTitleID()`| Int
|getEntryPointAddress()| returns the Entry point of the currently running app | `gecko.getEntryPointAddress()`| Hex
|runKernelCopyService()| | `gecko.runKernelCopyService()`| None
||||
|search()| Allows you to do a very simple search | `gecko.search(startAddress, value, length)`| Hex
|advancedSearch()| Allows you to do more advanced searches. | `gecko.advancedSearch(start, length, value, kernel, limit, aligned = 1)`| Hex (Table)
||||
|getSymbol()| Allows you to get the address of a function on the console | `gecko.getSymbol(rplname, sysname, data = 0)`| Int (function pointer/function address)
|call()| Allows to execute functions on the console. Often used with getSymbol (see example) | `gecko.call(address, *args)`|  It all depends on the function executed
||||
|clearAssembly()| | `gecko.clearAssembly()`| None
|excecuteAssembly()| executes parsed assembly | `gecko.excecuteAssembly(assembly)`| None
|persistAssembly()| | `gecko.persistAssembly(assembly)`| None