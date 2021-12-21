class NoIpEnteredException(Exception): pass
class InvalidIpAddressException(Exception): pass
class ConnectionIsAlreadyInProgressException(Exception): pass
class ConnectionIsNotInProgressException(Exception): pass
class ConnectionErrorException(Exception): pass
class InvalidMemoryAreaException(Exception): pass
class InvalidLengthException(Exception): pass
class ReadMemoryException(Exception): pass
class TooManyArgumentsException(Exception): pass