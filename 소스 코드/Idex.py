from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import Format

class Idex:

    def __init__(self):
        self.code = "nop"
        #WB
        self.reg_write = 0
        self.memto_reg = 0
        #M
        self.branch = 0
        self.mem_read = 0
        self.mem_write = 0
        #ex
        self.regDst = 0
        self.aluOp1 = 0
        self.aluOp0 = 0
        self.aluSrc = 0

        self.pc = 0
        self.read_register1 = 0
        self.read_register2 = 0
        self.instruction_15_0 = "0000000000000000000000000000000000000000"
        self.instruction_20_16 = "00000"
        self.instruction_15_11 = "00000"

        self.register_rs = "00000"
        self.register_rt = "00000"
        self.register_rd = "00000"

        self.branch_pc = 0
        self.branch_zero = 0
        self.if_flush = 0

    def InitUI(self, app):
        #IDEX
        title = QLabel("ID/EX", app)
        title.move(1000, 150)
        title.setFont(QFont('Arial', 20))

        self.code_label = QLabel("Code : nop", app)
        self.code_label.move(1000, 200)

        wb = QLabel("WB : ", app)
        wb.move(1200, 150)

        self.wb = QLabel("00", app)
        self.wb.move(1350, 150)

        m = QLabel("M : ", app)
        m.move(1200, 170)

        self.m = QLabel("000", app)
        self.m.move(1350, 170)

        ex = QLabel("EX : ", app)
        ex.move(1200, 190)

        self.ex = QLabel("0000", app)
        self.ex.move(1350, 190)

        pc = QLabel("PC : ", app)
        pc.move(1200, 210)

        self.pc_label = QLabel("0xeeeeeeee", app)
        self.pc_label.move(1350, 210)

        read_data1 = QLabel("Read Data 1 : ", app)
        read_data1.move(1200, 230)

        self.read_data1 = QLabel("0xeeeeeeee", app)
        self.read_data1.move(1350, 230)

        read_data2 = QLabel("Read Data 2 : ", app)
        read_data2.move(1200, 250)

        self.read_data2 = QLabel("0xeeeeeeee", app)
        self.read_data2.move(1350, 250)

        instruction1 = QLabel("Instruction15-0 : ", app)
        instruction1.move(1200, 270)

        self.instruction1 = QLabel("00000000000000000000000000000000", app)
        self.instruction1.move(1350, 270)

        instruction2 = QLabel("Instruction20-16 : ", app)
        instruction2.move(1200, 290)

        self.instruction2 = QLabel("00000", app)
        self.instruction2.move(1350, 290)
        
        instruction3 = QLabel("Instruction15-11 : ", app)
        instruction3.move(1200, 310)

        self.instruction3 = QLabel("00000", app)
        self.instruction3.move(1350, 310)

        register_rs_label = QLabel("Register Rs : ", app)
        register_rs_label.move(1200, 330)

        self.register_rs_label = QLabel("00000", app)
        self.register_rs_label.move(1350, 330)

        register_rt_label = QLabel("Register Rt : ", app)
        register_rt_label.move(1200, 350)

        self.register_rt_label = QLabel("00000", app)
        self.register_rt_label.move(1350, 350)

        register_rd_label = QLabel("Register Rd : ", app)
        register_rd_label.move(1200, 370)

        self.register_rd_label = QLabel("00000", app)
        self.register_rd_label.move(1350, 370)

    def Reset(self):
        self.code = "nop"
        #WB
        self.reg_write = 0
        self.memto_reg = 0
        #M
        self.branch = 0
        self.mem_read = 0
        self.mem_write = 0
        #ex
        self.regDst = 0
        self.aluOp1 = 0
        self.aluOp0 = 0
        self.aluSrc = 0

        self.pc = 0
        self.read_register1 = 0
        self.read_register2 = 0
        self.instruction_15_0 = "0000000000000000000000000000000000000000"
        self.instruction_20_16 = "00000"
        self.instruction_15_11 = "00000"

        self.register_rs = "00000"
        self.register_rt = "00000"
        self.register_rd = "00000"

        self.branch_pc = 0
        self.branch_zero = 0
        self.if_flush = 0

        self.LabelUpdate()

    def Control(self, instruction):
        if instruction[0:6] == "000000":
            self.regDst = 1
            self.aluOp1 = 1
            self.aluOp0 = 0
            self.aluSrc = 0
            self.branch = 0
            self.mem_read = 0
            self.mem_write = 0
            self.reg_write = 1
            self.memto_reg = 0

        elif instruction[0:6] == "100011": #lw
            self.regDst = 0
            self.aluSrc = 1
            self.reg_write = 1
            self.memto_reg = 1
            self.mem_read = 1
            self.mem_write = 0
            self.branch = 0
            self.aluOp1 = 0
            self.aluOp0 = 0

        elif instruction[0:6] == "101011": #sw
            self.regDst = 0
            self.aluSrc = 1
            self.reg_write = 0
            self.memto_reg = 0
            self.mem_read = 0
            self.mem_write = 1
            self.branch = 0
            self.aluOp1 = 0
            self.aluOp0 = 0
            
        elif instruction[0:6] == "000100": #beq
            self.regDst = 0
            self.aluSrc = 0
            self.reg_write = 0
            self.memto_reg = 0
            self.mem_read = 0
            self.mem_write = 0
            self.branch = 1
            self.aluOp1 = 0
            self.aluOp0 = 1

        elif instruction[0:6] == "000010": #j
            self.regDst = 0
            self.aluSrc = 0
            self.reg_write = 0
            self.memto_reg = 0
            self.mem_read = 0
            self.mem_write = 0
            self.branch = 1
            self.aluOp1 = 0
            self.aluOp0 = 0

    def RisingEdge(self, ifid, ifid_write, registers):
        if ifid.code == "nop" or ifid_write == 0:
            self.Reset()
            return

        self.code = ifid.code

        self.Control(ifid.instruction)

        self.pc = ifid.pc

        self.read_register1 = registers.registers[int(ifid.instruction[6:11], 2)]
        self.read_register2 = registers.registers[int(ifid.instruction[11:16], 2)]

        sign = ["0000000000000000", "1111111111111111"][int(ifid.instruction[16])]
        self.instruction_15_0 = sign + ifid.instruction[16:32]
        self.instruction_15_11 = ifid.instruction[16:21]
        self.instruction_20_16 = ifid.instruction[11:16]
        self.register_rs = ifid.instruction[6:11]
        self.register_rt = ifid.instruction[11:16]
        self.register_rd = ifid.instruction[16:21]

        #branch hazard
        if ifid.instruction[0:6] == "000100": #beq 
            bta = int(self.instruction_15_0[2:], 2) << 2
            self.branch_pc = self.pc + bta - 4

        elif ifid.instruction[0:6] == "000010": #j
            bta = int(ifid.instruction[6:], 2) << 2
            self.branch_pc = bta - 4

        if self.read_register1 - self.read_register2 == 0:
            self.branch_zero = 1
        else:
            self.branch_zero = 0

        if (self.branch == 1 and self.branch_zero == 1) or ifid.instruction[0:6] == "000010":
            self.if_flush = 1
        else:
            self.if_flush = 0

        self.LabelUpdate()

    def LabelUpdate(self):
        self.code_label.setText("Code : " + self.code)
        self.code_label.setFixedWidth(500)

        self.wb.setText(str(self.reg_write) + str(self.memto_reg))
        self.m.setText(str(self.branch) + str(self.mem_read) + str(self.mem_write))
        self.ex.setText(str(self.regDst) + str(self.aluOp1) + str(self.aluOp0) + str(self.aluSrc))

        self.pc_label.setText(Format.HexFormat(self.pc))

        self.read_data1.setText(Format.HexFormat(self.read_register1))
        self.read_data1.setFixedWidth(300)

        self.read_data2.setText(Format.HexFormat(self.read_register2))
        self.read_data2.setFixedWidth(300)

        self.instruction1.setText(self.instruction_15_0)
        self.instruction2.setText(self.instruction_15_11)
        self.instruction3.setText(self.instruction_20_16)
        self.register_rs_label.setText(self.register_rs)
        self.register_rt_label.setText(self.register_rt)
        self.register_rd_label.setText(self.register_rd)