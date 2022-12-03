from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import Format

class Ifid:
    def __init__(self):
        self.pc = int("400024", 16)
        self.instruction = "00000000000000000000000000000000"
        self.code = "nop"

    def InitUI(self, app):
        title = QLabel("IF/ID", app)
        title.move(1000, 50)
        title.setFont(QFont('Arial', 20))

        self.codeLabel = QLabel("Code : nop", app)
        self.codeLabel.move(1000, 100)

        pc_label = QLabel("PC :", app)
        pc_label.move(1200, 50)

        self.pc_label = QLabel("0x00000000", app)
        self.pc_label.move(1350, 50)

        instruction_label = QLabel("Instruction : ", app)
        instruction_label.move(1200, 70)

        self.instruction_label = QLabel("00000000000000000000000000000000", app)
        self.instruction_label.move(1350, 70)

    def Reset(self):
        self.pc = int("400024", 16)
        self.instruction = "00000000000000000000000000000000"
        self.code = "nop"

        self.LabelUpdate()

    def RisingEdge(self, idex, write, instruction):

        if write == 0:
            return

        if Format.HexFormat(int(self.pc)) in instruction.binarys.keys():
            self.instruction = instruction.binarys[Format.HexFormat(int(self.pc))]
            self.code = instruction.codes[(self.pc - int("400024", 16)) // 4]
        else:
            self.instruction = "00000000000000000000000000000000"
            self.code = "nop"
        
        if idex.if_flush == 1:
            self.pc = idex.branch_pc
            self.instruction = "00000000000000000000000000000000"
            self.code = "nop"
        else:
            self.pc = self.pc + 4

        self.LabelUpdate()

    def LabelUpdate(self):
        self.codeLabel.setText("Code : " + self.code)
        self.codeLabel.setFixedWidth(300)

        self.pc_label.setText(format(int(self.pc), "#x"))
        self.pc_label.setFixedWidth(100)

        self.instruction_label.setText(self.instruction)
        self.instruction_label.setFixedWidth(500)

