from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import Format

class Memwb:
    
    def __init__(self):
        self.code = "nop"

        self.reg_write = 0
        self.memto_reg = 0

        self.read_data = 0
        self.alu_result = 0
        self.register_rd = "00000"

    def InitUI(self, app):
        title = QLabel("MEM/WB", app)
        title.move(1000, 600)
        title.setFont(QFont('Arial', 20))

        self.code_label = QLabel("PC : nop", app)
        self.code_label.move(1000, 650)

        wb_label = QLabel("WB : ", app)
        wb_label.move(1200, 600)

        self.wb_label = QLabel("00", app)
        self.wb_label.move(1350, 600)

        read_data_label = QLabel("Read Data : ", app)
        read_data_label.move(1200, 620)

        self.read_data_label = QLabel("0xeeeeeeee", app)
        self.read_data_label.move(1350, 620)

        alu_label = QLabel("ALU : ", app)
        alu_label.move(1200, 640)

        self.alu_label = QLabel("0xeeeeeeee", app)
        self.alu_label.move(1350, 640) 

        write_register_label = QLabel("Register rd : ", app)
        write_register_label.move(1200, 660)

        self.write_register_label = QLabel("00000", app)
        self.write_register_label.move(1350, 660)

    def Reset(self):
        self.code = "nop"

        self.reg_write = 0
        self.memto_reg = 0

        self.read_data = 0
        self.alu_result = 0
        self.register_rd = "00000"
        
        self.LabelUpdate()

    def RisingEdge(self, ifid, exmem, memory):

        self.code = exmem.code

        self.reg_write = exmem.reg_write
        self.memto_reg = exmem.memto_reg

        #메모리 읽기
        if exmem.mem_read == 1:
            if exmem.alu_result in memory.datas.keys():
                self.read_data = 0
                self.read_data += memory.datas[exmem.alu_result]
                self.read_data += memory.datas[exmem.alu_result + 1] * pow(16, 2)
                self.read_data += memory.datas[exmem.alu_result + 2] * pow(16, 4)
                self.read_data += memory.datas[exmem.alu_result + 3] * pow(16, 6)
            else:
                self.read_data = 0
        else:
            self.read_data = 0

        #메모리 쓰기
        if exmem.mem_write == 1:
            if exmem.alu_result in memory.datas.keys():
                d = exmem.mem_write_data
                memory.datas[exmem.alu_result] = d % 256
                d //= 256
                memory.datas[exmem.alu_result + 1] = d % 256
                d //= 256
                memory.datas[exmem.alu_result + 2] = d % 256
                d //= 256
                memory.datas[exmem.alu_result + 3] = d % 256

                memory.LabelUpdate()

        self.alu_result = exmem.alu_result
        self.register_rd = exmem.register_rd
        self.LabelUpdate()

    def LabelUpdate(self):
        self.code_label.setText("Code : " + self.code)
        self.code_label.setFixedWidth(500)

        self.wb_label.setText(str(self.reg_write) + str(self.memto_reg))
        self.read_data_label.setText(Format.HexFormat(self.read_data))

        self.alu_label.setText(Format.HexFormat(self.alu_result))
        self.write_register_label.setText(self.register_rd)
        self.write_register_label.setFixedWidth(100)
