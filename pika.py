from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit
import sys
import random

class Pika(QMainWindow):
    def __init__(self):
        super(Pika, self).__init__()
        self.setGeometry(200, 200, 1500, 1000)
        self.setWindowTitle("Pika")
        self.initUI()
        self.h2p = True
        self.input = ''
        self.output = ''
    
    def initUI(self):
        self.translate_button = QtWidgets.QPushButton(self)
        self.translate_button.setText("翻译")
        self.translate_button.clicked.connect(self.Translate)
        self.translate_button.move(700, 450)

        self.label_input = QtWidgets.QLabel(self)
        self.label_input.setText("Human Language")
        self.label_input.move(300, 200)

        self.label_output = QtWidgets.QLabel(self)
        self.label_output.setText("Pika Language")
        self.label_output.move(1100, 200)

        self.exchange_button = QtWidgets.QPushButton(self)
        self.exchange_button.setText("🔁")
        self.exchange_button.clicked.connect(self.Exchange)
        self.exchange_button.move(700, 500)

        self.text_input = QTextEdit(self)  # 创建文本框
        self.text_input.setPlaceholderText("你想要说什么呀")  # 设置提示信息
        self.text_input.resize(500, 500)
        self.text_input.move(150, 250)

        self.text_output = QTextEdit(self)
        self.text_output.setPlaceholderText("皮卡皮卡")
        self.text_output.resize(500, 500)
        self.text_output.move(900, 250)
        
        self.clipboard = QApplication.clipboard()
        self.copy_button = QtWidgets.QPushButton(self)
        self.copy_button.setText("复制到剪贴板")
        self.copy_button.clicked.connect(self.Copy)
        self.copy_button.move(1250, 800)

        self.clear_button = QtWidgets.QPushButton(self)
        self.clear_button.setText("清空")
        self.clear_button.clicked.connect(self.Clear)
        self.clear_button.move(700, 550)


        self.Update()
    
    def Translate(self):
        self.input = text_input = self.text_input.toPlainText()
        if self.h2p:
            self.output = h2pika(self.input)
            self.text_output.setText(self.output)
        else:
            self.output = pika2h(self.input)
            self.text_output.setText(self.output)

    def Update(self):
        self.label_input.adjustSize()
        self.label_output.adjustSize()
        self.copy_button.adjustSize()

    def Exchange(self):
        if self.h2p:
            self.label_input.setText("Pika Language")
            self.label_output.setText("Human Language")
        else:
            self.label_input.setText("Human Language")
            self.label_output.setText("Pika Language")
        self.h2p = not self.h2p
        self.text_input.setText(self.output)
        self.text_output.setText(self.input)
        self.input, self.output = self.output, self.input
        self.Update()

    def Copy(self):
        self.clipboard.setText(self.output)

    def Clear(self):
        self.text_input.clear()
        self.text_output.clear()
        self.input = ''
        self.output = ''



def window():
    app = QApplication(sys.argv)
    win = Pika()
    win.show()
    sys.exit(app.exec_())

# 字符串转二进制
def str_2_bin(str):
    # 输出仍以字符串的形式输出
    return ' '.join([bin(ord(c)).replace('0b', '') for c in str])

# 二进制转字符串
def bin_2_str(bin):
    return ''.join([chr(i) for i in [int(b, 2) for b in bin.split(' ')]])

# 二进制转皮卡丘语
def bin2pika(bin):
  """
  :param bin: 二进制字符串
  转换规则：0转为\u200d，1转为\u200b，空格转为\u200c
  :return: 皮卡丘语（零宽字符）
  """
  pika = ''
  for i in bin:
    if i == '1':
      pika += '\u200b'
    elif i == '0':
      pika += '\u200d'
    else:
      pika += '\u200c'
  return pika

# 皮卡丘语转二进制
def pika2bin(pika):
  """
  :param pika: 皮卡丘语（字符串）
  转换规则：\u200d转为0，\u200b转为1，\u200c转为空格
  :return: 二进制字符串
  """
  bin = ''
  for i in pika:
    if i == '\u200b':
      bin += '1'
    elif i == '\u200c':
      bin += ' '
    else: bin += '0'
  return bin

# 皮卡丘语词典
pika_dic = ['皮卡', '皮卡皮', '皮卡皮卡', '皮卡丘']

# 人类语言转皮卡丘语
def h2pika(h):
  pika = ''
  
  # 先将字符串转为二进制，再转为皮卡丘语前缀中的零宽字符
  bin = str_2_bin(h)
  pika += bin2pika(bin)
  
  # 皮卡丘语前缀后面的部分
  l = len(h)
  while True:
    # 少于四个字时，直接转为对应长度的皮卡丘语
    if l <= 2:
      pika += '皮卡 '
    elif l <= 3:
      pika += '皮卡皮 '
    elif l <= 4:
      pika += '皮卡皮卡 '
    # 多于四个字时，随机选择皮卡丘语
    l -= 4
    if l > 0:
      n = random.randint(0, 3)
      pika += (pika_dic[n] + ' ')
    else:
      break

  return pika

# 零宽字符列表
zwsp = ['\u200b', '\u200c', '\u200d']

# 皮卡丘语转人类语言
def pika2h(pika):
  ZW = ''
  for i in pika:
    if i in zwsp:
      ZW += i
  bin = pika2bin(ZW)
  # print(bin)
  h = bin_2_str(bin)

  return h

if __name__ == '__main__':
    window()