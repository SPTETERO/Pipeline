from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import Format

class Registers:

    def __init__(self):
        self.register_texts = ["$0", "$1", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3", "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7", "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"]
        self.register_connect = {"$0" : 0, "$1" : 1, "$v0" : 2, "$v1" : 3, "$a0" : 4, "$a1" : 5, "$a2" : 6, "$a3" : 7, "$t0" : 8, "$t1" : 9, "$t2" : 10, "$t3" : 11, "$t4" : 12, "$t5" : 13, "$t6" : 14, "$t7" : 15, "$s0" : 16, "$s1" : 17, "$s2" : 18, "$s3" : 19, "$s4" : 20, "$s5" : 21, "$s6" : 22, "$s7" : 23, "$t8" : 24, "$t9" : 25, "$k0" : 26, "$k1" : 27, "$gp" : 28, "$sp" : 29, "$fp" : 30, "$ra" : 31,
                                                      "$2" : 2, "$3" : 3, "$4" : 4, "$5" : 5, "$6" : 6, "$7" : 7, "$8" : 8, "$9" : 9, "$10" : 10, "$11" : 11, "$12" : 12, "$13" : 13, "$14" : 14, "$15" : 15, "$16" : 16, "$17" : 17,"$18" : 18, "$19" : 19, "$20" : 20, "$21" : 21, "$22" : 22, "$23" : 23, "$24" : 24, "$25" : 25,"$26" : 26, "$27" : 27, "$28" : 28, "$29" : 29, "$30" : 30, "$31" : 31 } 
        self.registers = [_ for _ in range(32)] 

        self.register_value_labels = []
        self.pc = int("400034", 16)

        self.clock = 0


    def InitUI(self, app):
        #self.pc_label = QLabel("PC", app)
        #self.pc_label.move(30, 40)
#
        #self.pc_label_value = QLabel("0xeeeeeeee", app)
        #self.pc_label_value.move(60, 40)
        #self.pc_label_value.setText(Format.HexFormat(self.pc))

        self.clock_label = QLabel("Clock : ", app)
        self.clock_label.move(30, 60)

        for i in range(32):
            register_label = QLabel(self.register_texts[i], app)
            register_label.move(30, 100 + i * 20)

            register_value_label = QLineEdit(app)
            register_value_label.move(60, 100 + i * 20)
            register_value_label.setFixedWidth(130)
            register_value_label.textChanged.connect(self.TextChange)
            self.register_value_labels.append(register_value_label)

        self.register_value_labels[29].setText("0x7ffffe40")
        self.register_value_labels[28].setText("0x10008000")
        
        self.LabelUpdate()

    def TextChange(self):
        for  i in range(len(self.register_value_labels)):
            register_value_label = self.register_value_labels[i]

            text = register_value_label.text()
            try:
                if "0x" in text:
                    self.registers[i] = int(text, 16)
                else:
                    self.registers[i] = int(text)
            except:
                self.registers[i] = 0
        self.LabelUpdate()

    def RisingEdge(self, memwb):
        if memwb.memto_reg == 1:
            write_data = memwb.read_data
        else:
            write_data = memwb.alu_result

        if memwb.reg_write == 1:
            registerId = int(memwb.register_rd, 2)
            self.registers[registerId] = write_data

        self.clock += 1
        
        self.LabelUpdate()

    def LabelUpdate(self):
       # self.pc_label_value.setText(Format.HexFormat(self.pc))
        for i in range(32):
            self.register_value_labels[i].setText(Format.HexFormat(self.registers[i]))

        self.clock_label.setText("Clock : " + str(self.clock)) 
        self.clock_label.setFixedWidth(500)