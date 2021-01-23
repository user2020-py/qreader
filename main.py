#Author: Matyoqubov Firdavs
import sys
from PyQt5.QtWidgets import QPushButton,QLabel,QPlainTextEdit,QMainWindow,QApplication
from PyQt5.QtGui import QPixmap,QIcon
import pyqrcode
import png
from PIL import Image
from pyzbar.pyzbar import decode
img = None

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        #self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle('QRCode')
        self.setGeometry(300, 200, 625, 368)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet('''QMainWindow{background: skyblue;}
                              QPushButton:hover{border: 1px solid red; background: skyblue}
                              QPushButton{border: 1px solid blue; background: white;}''') 
        #Widgets
        #=========
        self.encode = QPushButton('Create QR', self)
        self.encode.move(10,10)
        self.decode = QPushButton('Decode Image', self)
        self.decode.move(120,10)
        self.e = QPushButton('Exit App', self)
        self.e.move(230,10)
        #=========
        self.textarea = QPlainTextEdit(self)
        self.textarea.setGeometry(11, 48, 318, 308)
        self.textarea.setStyleSheet("border: 1px solid black;") 
        #=========
        self.label = QLabel(self) 
        self.pixmap = QPixmap('img\info.png') 
        self.label.setPixmap(self.pixmap)
        self.label.move(345, 10)
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        self.label.setStyleSheet("border: 1px solid black;")
        #=========
        self.save = QPushButton('Save QR', self)
        self.save.move(370,300)
        self.cl = QPushButton('Clear Text', self)
        self.cl.move(480,300)
        #=========

        #Events
        self.encode.clicked.connect(self.encode_text)
        self.save.clicked.connect(self.saveFileDialog)
        self.cl.clicked.connect(self.cl_text)
        self.e.clicked.connect(exit)
        self.decode.clicked.connect(self.decode_img)
        self.show()

    def encode_text(self):
        global img
        text=str(self.textarea.toPlainText())
        result=pyqrcode.create(text)
        result.png('qr_result.png', scale=9)
        img = result
        result.show()

    def saveFileDialog(self):
        global img
        self.setStyleSheet('''QPushButton{border: none; background: none;}''') 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save","qr_code","Save QRCode(png);", options=options)
        if fileName=='':
            pass
        else:
            img.png(str(fileName+'.png'), scale=9)
        self.setStyleSheet('''QMainWindow{background: skyblue;}
                              QPushButton:hover{border: 1px solid red; background: skyblue}
                              QPushButton{border: 1px solid blue; background: white;}''')
    def cl_text(self):
        self.textarea.clear()
    
    def decode_img(self):
        self.setStyleSheet('''QPushButton{border: none; background: none;}''')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileNames(self,"Open","","Open QRCode (*.png)", options=options)
        if fileName==[]:
            pass
        else:
            data = decode(Image.open(str(fileName[0])))
            self.textarea.clear()
            self.textarea.insertPlainText(str(data[0].data).strip("b'"))
            
        self.setStyleSheet('''QMainWindow{background: skyblue;}
                              QPushButton:hover{border: 1px solid red; background: skyblue}
                              QPushButton{border: 1px solid blue; background: white;}''')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
