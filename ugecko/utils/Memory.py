
class Memory:
    def validRange(address: int, length: int) -> bool:
        if   0x01000000 <= address and address + length <= 0x01800000: return True
        elif 0x0E000000 <= address and address + length <= 0x10000000: return True
        elif 0x10000000 <= address and address + length <= 0x50000000: return True
        elif 0xE0000000 <= address and address + length <= 0xE4000000: return True
        elif 0xE8000000 <= address and address + length <= 0xEA000000: return True
        elif 0xF4000000 <= address and address + length <= 0xF6000000: return True
        elif 0xF6000000 <= address and address + length <= 0xF6800000: return True
        elif 0xF8000000 <= address and address + length <= 0xFB000000: return True
        elif 0xFB000000 <= address and address + length <= 0xFB800000: return True
        elif 0xFFFE0000 <= address and address + length <= 0xFFFFFFFF: return True
        else: return False

    def validAccess(address: int, length: int, access: str) -> bool:
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

    def isValidMemoryArea(address: int, length: int, skip_verification: bool = False, mode: str = "write") -> bool:
        if not skip_verification:
            if not Memory.validRange(address, length): return False
            if not Memory.validAccess(address, length, mode): return False
        return True