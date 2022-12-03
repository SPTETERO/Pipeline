from PyQt5.QtWidgets import QLabel


import Format


class Memory:

    def __init__(self):
        self.datas = {4194304 + i : 0 for i in range(400)}
        self.memory_label = []
        self.cursor = 0

    def AddByte(self, data):
        self.datas[4194304 + self.cursor] = data
        self.cursor += 1

    def LabelUpdate(self):

        for i in range(45):
            num = self.datas[4194304 + i * 4]
            num += pow(16 * 16, 1) * self.datas[4194304 + i * 4 + 1]
            num += pow(16 * 16, 2) * self.datas[4194304 + i * 4 + 2]
            num += pow(16 * 16, 3) * self.datas[4194304 + i * 4 + 3]

            self.memory_label[i].setText(Format.HexFormat(num))