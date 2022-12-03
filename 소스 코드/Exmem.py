from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import Format

class Exmem:

    def __init__(self):
        self.code = "nop"
        #WB
        self.reg_write = 0
        self.memto_reg = 0
        #M
        self.branch = 0
        self.mem_read = 0
        self.mem_write = 0

        self.pc = 0
        self.zero = 0
        self.alu_result = 0
        self.mem_write_data = 0
        self.register_rd = "00000"

    def InitUI(self, app):
        #IDEX
        title = QLabel("EX/MEM", app)
        title.move(1000, 400)
        title.setFont(QFont('Arial', 20))

        self.code_label = QLabel("Code : nop", app)
        self.code_label.move(1000, 450)

        wb_label = QLabel("WB : ", app)
        wb_label.move(1200, 400)

        self.wb_label = QLabel("00", app)
        self.wb_label.move(1350, 400)

        m_label = QLabel("M : ", app)
        m_label.move(1200, 420)

        self.m_label = QLabel("000", app)
        self.m_label.move(1350, 420)

        pc_label = QLabel("PC : ", app)
        pc_label.move(1200, 440)

        self.pc_label = QLabel("0xeeeeeeee", app)
        self.pc_label.move(1350, 440)

        zero_label = QLabel("Zero : ", app)
        zero_label.move(1200, 460)

        self.zero_label = QLabel("0", app)
        self.zero_label.move(1350, 460)

        alu_label = QLabel("ALU : ", app)
        alu_label.move(1200, 480)

        self.alu_label = QLabel("0xeeeeeeee", app)
        self.alu_label.move(1350, 480)

        mem_write_label = QLabel("Memory Write Data : ", app)
        mem_write_label.move(1200, 500)

        self.mem_write_label = QLabel("0xeeeeeeee", app)
        self.mem_write_label.move(1350, 500)

        writeRegister = QLabel("Register rd : ", app)
        writeRegister.move(1200, 520)

        self.register_rd_label = QLabel("00000", app)
        self.register_rd_label.move(1350, 520)

    def Reset(self):
        self.code = "nop"
        #WB
        self.reg_write = 0
        self.memto_reg = 0
        #M
        self.branch = 0
        self.mem_read = 0
        self.mem_write = 0

        self.pc = 0
        self.zero = 0
        self.alu_result = 0
        self.mem_write_data = 0
        self.register_rd = "00000"

    def AluControl(self, aluop1, aluop0, function):
        if aluop0 == 0 and aluop1 == 0:
            return "0010"
        if aluop0 == 0 and aluop1 == 1:
            return "0110"
        if aluop0 == 1 and aluop1 == 0:
            
            if function == "100000":
                return "0010"
            elif function == "100010":
                return "0110"
            elif function == "100100":
                return "0000"
            elif function == "100101":
                return "0001"
            elif function == "101010":
                return "0111"

    def Alu(self, data1, data2, control):
        result = 0
        if control == "0000":
            result = data1 & data2

        elif control == "0001":
            result = data1 | data2

        elif control == "0010":
            result = data1 + data2

        elif control == "0110":
            result = data1 - data2

        elif control == "0111":
            d = data1 - data2
            if d < 0:
                return 0, 0
            elif d == 0:
                return 0, 1
            else:
                return 1, 1
                
        elif control == "1100":
            pass #nor 연산
        
        if result == 0:
            zero = 1
        else:
            zero = 0

        return result, zero

    def ForwardingUnit(self, register_rs, register_rt, exmem_rd, memwb_rd, idex, memwb):
        forwardA = 0
        if register_rs == exmem_rd:
            forwardA = 1
        elif register_rs == memwb_rd:
            forwardA = 2

        forwardB = 0
        if register_rt == exmem_rd:
            forwardB = 1
        elif register_rt == memwb_rd:
            forwardB = 2
        
        if forwardA == 0:
            data1 = idex.read_register1
        elif forwardA == 1:
            data1 = self.alu_result
        elif forwardA == 2:
            if memwb.memto_reg == 1:
                data1 = memwb.read_data
            else:
                data1 = memwb.alu_result    

        if forwardB == 0:
            if idex.aluSrc == 0:
                data2 = idex.read_register2
            else:
                data2 = int(idex.instruction_15_0, 2)
        elif forwardB == 1:
            data2 = self.alu_result
        elif forwardB == 2:
            if memwb.memto_reg == 1:
                data2 = memwb.read_data
            else:
                data2 = memwb.alu_result   

        return data1, data2

    def RisingEdge(self, idex, memwb):

        if idex.code == "":
            return

        self.code = idex.code

        #wb
        self.reg_write = idex.reg_write
        self.memto_reg = idex.memto_reg
        #m
        self.branch = idex.branch
        self.mem_read = idex.mem_read
        self.mem_write = idex.mem_write

        #bta = int(idex.instruction_15_0[2:], 2) << 2
        #self.pc = idex.pc + bta

        #Forward
        data1, data2 = self.ForwardingUnit(idex.register_rs, idex.register_rt, self.register_rd, memwb.register_rd, idex, memwb)
        #ALU Control
        alu_control = self.AluControl(idex.aluOp0, idex.aluOp1, idex.instruction_15_0[-6:])

        self.alu_result, self.zero = self.Alu(data1, data2, alu_control)

        self.mem_write_data = idex.read_register2

        if idex.regDst == 0:
            self.register_rd = idex.instruction_20_16
        else:
            self.register_rd = idex.instruction_15_11

        self.LabelUpdate()

    def LabelUpdate(self):
        self.code_label.setText("Code : " + self.code)
        self.code_label.setFixedWidth(500)

        self.register_rd_label.setText(self.register_rd)
        
        self.wb_label.setText(str(self.reg_write) + str(self.memto_reg))
        self.m_label.setText(str(self.branch) + str(self.mem_read) + str(self.mem_write))

        self.pc_label.setText(Format.HexFormat(self.pc))
        self.zero_label.setText(str(self.zero))
        self.alu_label.setText(Format.HexFormat(self.alu_result))
        self.mem_write_label.setText(Format.HexFormat(self.mem_write_data))

