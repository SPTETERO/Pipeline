from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import Format

class Ifid:
    def __init__(self):
        self.pc = int("400024", 16)
        self.instruction = "00000000000000000000000000000000"
        self.code = "nop"

    def InitUI(self, app):
        self.codeLabel = QLabel("nop", app)
        self.codeLabel.setFont(QFont('Arial', 20))
        self.codeLabel.move(920, 0)

        font = QFont('Arial', 9)
        font.setBold(True)

        self.pc_label = QLabel("0x00000000", app)
        self.pc_label.move(1040, 360)
        self.pc_label.setFont(font)

        self.instruction_label = QLabel("00000000000000000000000000000000", app)
        self.instruction_label.move(880, 620)
        self.instruction_label.setFont(font)

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
        self.codeLabel.setText("" + self.code)
        self.codeLabel.setFixedWidth(300)

        self.pc_label.setText(format(int(self.pc), "#x"))
        self.pc_label.setFixedWidth(100)

        self.instruction_label.setText(self.instruction)
        self.instruction_label.setFixedWidth(500)

