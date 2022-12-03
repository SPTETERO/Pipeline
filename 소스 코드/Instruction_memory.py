import Registers
import Memory

import Format

class Instruct_memory:

    def __init__(self):
        self.binarys = {}
        self.codes = []
        self.codeAddress = {}


    def ToBinary(self, size, n):
        result = ""
        for _ in range(size):
            if n % 2 == 1:
                result += "1"
            else:
                result += "0"
 
            n //= 2

        result = list(result)
        result.reverse()
        result = "".join(result)
        return result


    def StrBinToNum(self, bin):
        result = 0
        bin = list(bin)
        bin.reverse()
        c = 1

        for i in range(32):
            result += c * int(bin[i])
            c *= 2

        return result

    def Assembly(self, register, memory, texts):
        self.binarys = {}
        self.codes = []
        self.codeAddress = {}
        memory_on = False
        codeStart = 0

        for i in range(len(texts)):
            line = texts[i]
            if ".text" in line:
                codeStart = i

            data = line.replace(',', '').split()
            if ":" in line:
                self.codeAddress[data[0]] = Format.HexFormat(int("400024", 16) + (i - codeStart - 1) * 4)

        for line in texts:
            line = line.strip()
            if line == "":
                continue

            if line == ".data":
                memory_on = True
                continue

            if line == ".text":
                memory_on = False
                continue

            if ".global" in line:
                continue

            if memory_on:
                data = line.split()
                if data[0] == ".byte":
                    d = 0
                    if "'" in data[1]:
                        data[1] = data[1].replace("'", "")
                        d = ord(data[1])

                    else:
                        d = int(data[1])

                    memory.AddByte(d)

                elif data[0] == ".space":
                    for _ in range(int(data[1])):
                        memory.AddByte(0)

                elif data[0] == ".word":
                    for _ in range([0, 3, 2, 1][len(memory.datas) % 4]):
                        memory.AddByte(0)

                    if '0x' in data[1]:
                        d = int(data[1], 16)
                    else:
                        d = int(data[1])

                    for i in range(4):
                        memory.AddByte(d % 256)
                        d //= 256

                elif data[0] == ".ascii":
                    for _ in range([0, 3, 2, 1][len(memory.datas) % 4]):
                        memory.AddByte(0)

                    data[1] = data[1].replace('"', "")
                    for c in data[1]: 
                        memory.AddByte(ord(c))

                elif data[0] == ".asciiz":
                    for _ in range([0, 3, 2, 1][len(memory.datas) % 4]):
                        memory.AddByte(0)

                    data[1] = data[1].replace('"', "")
                    for c in data[1]:
                        memory.AddByte(ord(c))

                    memory.AddByte(ord("\0"))

            else:
                if ":" in line:
                    line = line[line.index(":") + 1:].strip()

                binary = ""
                data = line.replace(',', '').split()
                op = data[0]
                rs = 0
                rt = 0
                rd = 0
                shamt = 0
                funct = 0

                #R format                
                if op in ["add", "sub", "and", "or", "slt"]:
                    funct_data = {"add" : 32, "sub" : 34, "and" : 36, "or" : 37, "slt" : 42}
                    funct = funct_data[op]

                    op = 0
                    rs = register.register_connect[data[2].strip()]
                    rt = register.register_connect[data[3].strip()]
                    rd = register.register_connect[data[1].strip()]
                    shamt = 0

                    binary = self.ToBinary(6, op) + self.ToBinary(5, rs) + self.ToBinary(5, rt) + self.ToBinary(5, rd) + self.ToBinary(5, shamt) + self.ToBinary(6, funct)

                #data format
                if op in ["lw", "sw"]:
                    op_data = {"lw" : 35, "sw" : 43}
                    op = op_data[op]
                    rs = register.register_connect[data[2].strip().split('(')[1][:-1]]
                    rt = register.register_connect[data[1].strip()]
                    constant = int(data[2].strip().split('(')[0])

                    binary = self.ToBinary(6, op) + self.ToBinary(5, rs) + self.ToBinary(5, rt) + self.ToBinary(16, constant)

                if op in ["beq"]:
                    op_data = {"beq" : 4}
                    op = op_data[op]
                    rs = register.register_connect[data[1].strip()]
                    rt = register.register_connect[data[2].strip()]
                    bta = (int(self.codeAddress[data[3].strip()], 16) - (int("400024", 16) + len(self.binarys) * 4)) >> 2
                    bta -= 1

                    binary = self.ToBinary(6, op) + self.ToBinary(5, rs) + self.ToBinary(5, rt) + self.ToBinary(16, bta)

                if op in ["j"]:
                    op_data = {"j" : 2}
                    op = op_data[op]
                    bta = int(self.codeAddress[data[1].strip()], 16) >> 2

                    binary = self.ToBinary(6, op) + self.ToBinary(26, bta)

                self.codes.append(line)
                self.binarys[Format.HexFormat(int("400024", 16) + len(self.binarys) * 4)] = binary

        memory.LabelUpdate()
        return self.binarys, self.codes