from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout,\
    QProgressBar, QLabel

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from subprocessThread import subprocessThread


class ProcessDialog(QDialog):
    """
    实现功能：自动识别并分割基桩
    """
    # 发送子进程所返回结果(id,x,y,r)
    resultSignal = pyqtSignal(int, int, int, int)
    # 发送子进程结束的信号
    endSignal = pyqtSignal()

    def __init__(self,parent=None):
        super(ProcessDialog, self).__init__(parent)
        self.__initVariable()
        self.__initUI()


    def __initVariable(self):
        self.progressFile = './modules/example.exe'
        self.thread = None
        self.count = 0
        self.totalCount = 0


    def __initUI(self):
        startButton = QPushButton('开始')
        startButton.pressed.connect(self.__startRun)
        stopButton = QPushButton('停止')
        stopButton.pressed.connect(self.__stopRun)

        startButton.setStyleSheet('''
            QPushButton{
                height: 30px;
                width: 90px;
                padding-top: 4px;
                padding-bottom: 4px;
                color: white;
                font: bold;
                background-color: #0c75ff;
                border: none;
            }
            QPushButton:hover{
                background-color: #2a86fe;
            }
            QPushButton:pressed{
                padding-left: 5px;
                padding-top: 6px;
                background: #2a86fe;
            }
        ''')
        stopButton.setStyleSheet('''
            QPushButton{
                height: 30px;
                width: 90px;
                padding-top: 4px;
                padding-bottom: 4px;
                color: white;
                font: bold;
                background-color: #e3195c;
                border: none;
            }
            QPushButton:hover{
                background-color: #f6286c;
            }
            QPushButton:pressed{
                padding-left: 5px;
                padding-top: 6px;
                background: #f6286c;
            }
        ''')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(startButton)
        hbox1.addStretch(1)
        hbox1.addWidget(stopButton)

        margin = 20
        vbox = QVBoxLayout()
        vbox.setContentsMargins(margin, margin, margin, margin)

        self.textLabel = QLabel('')
        
        self.progress = QProgressBar()
        self.progress.setValue(0)

        vbox.addLayout(hbox1)
        vbox.addSpacing(margin / 2)
        vbox.addWidget(self.textLabel)
        vbox.addSpacing(margin / 4)
        vbox.addWidget(self.progress)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.resize(400, 150)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Example Process Dialog')

        self.setStyleSheet("""
            *{  
                color: #555555;
                font-size: 15px;
                font-family: DejaVu Sans, Microsoft YaHei;
                background: white;
            }
            QLabel{
                font-size:14px;
            }
            /***********QProgressBar***********/
            QProgressBar{
                text-align: center;
                color: #333333;
                background: #f4fef6;
                height: 15px;
                border: 1px solid #4cdb64;
            }
            QProgressBar::chunk{
                background-color: #4cdb64; 
            } 
        """)

    # 开始子进程
    def __startRun(self):
        if self.thread is not None:
            return

        # 选取当前选择的算法
        methodIdx = self.selectMethodsCombox.currentIndex()

        self.thread = subprocessThread()
        self.thread.setInputInfo(self.programFile)
        self.thread.ThreadResult.connect(self.updateShow)

        self.thread.start()

    # 停止子线程
    def __stopRun(self):
        if self.thread is None:
            return

        self.thread.stop()
        self.thread.terminate()
        del self.thread

        self.thread = None
        self.count = 0


    # 关掉窗口
    def closeEvent(self,event):
        if self.thread is not None:
            self.thread.stop()

        super().closeEvent(event)

    # 读取子进程返回的数据
    def updateShow(self, info):
        if 'num' in info:
            self.totalCount=int(info.split(':')[-1])
            self.progress.setMinimum(0)
            self.progress.setMaximum(self.totalCount)
        elif 'OK' in info:
            self.textLabel.setText('完成')
            self.endSignal.emit()
        else:
            self.count=self.count+1
            self.textLabel.setText('第'+str(self.count)+'个')
            self.progress.setValue(self.count)

            item = info.split(',')
            if '' not in item and len(item) == 5:
                index = int(item[0])
                px = int(item[1])
                py = int(item[2])
                pr = int(item[3])
                flag = int(item[4])

                if flag == 1:
                    self.resultSignal.emit(index, px, py, pr)





if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    viewer = processDialog()
    viewer.show()

    sys.exit(app.exec_())
