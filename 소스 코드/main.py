import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from Memory import Memory
from Instruction_memory import Instruct_memory
from Registers import Registers

from Ifid import Ifid
from Idex import Idex
from Exmem import Exmem
from Memwb import Memwb

import Format

class Application(QWidget):

    def __init__(self):
        super().__init__()

        self.instruction = Instruct_memory()
        self.datamemory = Memory()

        self.setWindowTitle("Spim")
        self.move(10, 10)
        self.resize(2000, 1000)

        self.ButtonUI()
        self.InstructionUI()
        self.MemoryUI()
        
        self.registers = Registers()
        self.registers.InitUI(self)

        pipeline_img = QPixmap('Pipeline1.png')
        pipeline = QLabel(self)
        pipeline.setPixmap(pipeline_img)
        pipeline.move(800, 30)


        self.ifid = Ifid()
        self.ifid.InitUI(self)

        self.idex = Idex()
        self.idex.InitUI(self)

        self.exmem = Exmem()
        self.exmem.InitUI(self)

        self.memwb = Memwb()
        self.memwb.InitUI(self)

        self.show()

    def ButtonUI(self):
        btn = QPushButton("열기", self)
        btn.move(200, 10)
        btn.clicked.connect(self.FileOpen)

        btn = QPushButton("Rising Edge", self)
        btn.move(300, 10)
        btn.clicked.connect(self.RisingEdge)


    def InstructionUI(self):
        self.codePc_labels = []
        self.binary_labels = []
        self.code_labels = []

        for i in range(45):
            codePc_label = QLabel("[00000000]", self)
            codePc_label.move(200, 50 + i * 20)
            codePc_label.setText(Format.HexFormat(int("400024", 16) + i * 4))
            self.codePc_labels.append(codePc_label)

            binary_label = QLabel("0xeeeeeeee", self)
            binary_label.move(300, 50 + i * 20)
            self.binary_labels.append(binary_label)

            code_label = QLabel("--------------------------", self)
            code_label.move(400, 50 + i * 20)
            self.code_labels.append(code_label)

    def MemoryUI(self):
        self.memoryAddress = []

        memoryText = QLabel("MEMORY", self)
        memoryText.move(550, 20)

        for i in range(45):
            memoryAddress = QLabel("[0xeeeeeeee]", self)
            memoryAddress.move(550, 50 + i * 20)
            memoryAddress.setText(Format.HexFormat(4194304 + i * 4))
            self.memoryAddress.append(memoryAddress)
    
            memoryValue = QLabel("0xeeeeeeee", self)
            memoryValue.move(650, 50 + i * 20)
            self.datamemory.memory_label.append(memoryValue)

    def FileOpen(self):
        file = QFileDialog.getOpenFileName(self, "Open FIle", "./", "(*.s)")
        f = open(file[0], "r", encoding="UTF8")
        code = []

        while True:
            line = f.readline()
            if not line:
                break
            code.append(line)

        assamblyCode, codes = self.instruction.Assembly(self.registers, self.datamemory, code)
        
        for i in range(45):
            if i < len(assamblyCode):
                self.codePc_labels[i].setText(Format.HexFormat(int("400024", 16) + i * 4))
                self.binary_labels[i].setText(Format.HexFormat(self.instruction.StrBinToNum(assamblyCode[Format.HexFormat(int("400024", 16) + i * 4)])))
                self.code_labels[i].setText(codes[i])
            else:
                self.codePc_labels[i].setText("")
                self.binary_labels[i].setText("")
                self.code_labels[i].setText("")

        self.ifid.Reset()
        self.idex.Reset()
        self.exmem.Reset()
        self.memwb.Reset()
        self.registers.clock = 0

        f.close()
    
    def HarzardDetectionUnit(self):
        ifid_write = 0  

        ifid_register_rs = self.ifid.instruction[6:11]
        ifid_register_rt = self.ifid.instruction[11:16]
        ifid_register_rd = self.ifid.instruction[16:21]

        if (self.idex.mem_read == 1 and (self.idex.register_rt == ifid_register_rs or self.idex.register_rt == ifid_register_rt)) or ("lw" in self.memwb.code and self.ifid.instruction[0:6] in ["000100", "000010"]):
            self.idex.regDst = 0
            self.idex.aluSrc = 0
            self.idex.reg_write = 0
            self.idex.memto_reg = 0
            self.idex.mem_read = 0
            self.idex.mem_write = 0
            self.idex.branch = 0
            self.idex.aluOp1 = 0
            self.idex.aluOp0 = 0
            self.idex.code == "Bubble"
        else:
            ifid_write = 1
        return ifid_write


    def RisingEdge(self):
        self.registers.RisingEdge(self.memwb)
        self.memwb.RisingEdge(self.ifid, self.exmem, self.datamemory)
        self.exmem.RisingEdge(self.idex, self.memwb)
        ifid_write = self.HarzardDetectionUnit()
        self.idex.RisingEdge(self.exmem, self.memwb, self.ifid, ifid_write, self.registers)
        self.ifid.RisingEdge(self.idex, ifid_write, self.instruction)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())
