from PyQt5.QtCore import QThread, pyqtSignal, Qt
from tempfile import NamedTemporaryFile
import codecs
import locale
import os
from subprocess import Popen
import subprocess


# 分割线程
class SubprocessThread(QThread):
    threadResult = pyqtSignal(str)

    def __init__(self):
        super(SubprocessThread, self).__init__()
        self.stopCommand = 'taskkill /F /IM '
        # 所调用的外部exe是否正在运行
        self.ExErunning = False

    # 设置
    def setInputInfo(self, programFile):
        self.programFile = programFile 

    # 强制结束执行 exe 文件或退出时操作
    def stop(self):
        if not self.ExErunning:
            return

        # 终止运行
        self.stopCommand += os.path.basename(self.programFile)

        if hasattr(self, "process"):
            self.process.kill()
            os.system(self.stopCommand)  # 调用外部命令结束

        self.ExErunning = False

    def run(self):
        # 输出结果的文件
        with NamedTemporaryFile('w+t', delete=False) as f:
            resultFile = f.name.replace("\\", '/')

        # 参数命令
        cmd = []
        cmd.append(self.programFile)
        cmd.append(resultFile)

        # 子线程的cmd窗口属性
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        # 开始运行 cpp 编译的 exe 文件
        self.ExErunning = True
        self.process = Popen(cmd, startupinfo=startupinfo, shell=True,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        # 踩坑点：只能自己设置条件判断是否输出结束，否则在data = self.process.stdout.readline()
        # 读到最后一行后，自动跳出循环，跳出整个run函数，而不执行后续的内容。
        totalCount = 1  # 所有点的个数
        endFlag = -1    # 结束标志
        while True:
            # 读取数据
            data = self.process.stdout.readline()
            data = data.decode(
                codecs.lookup(locale.getpreferredencoding()).name)

            self.threadResult.emit(data)

            # 第一条数据包含了输出行数信息，第一行的格式为“num:INT_N”
            if 'num' in data:
                totalCount = int(data.split(':')[-1])

            # 判断是否是最后一行，跳出循环（此处如果不判断会异常跳出）
            endFlag += 1
            if endFlag == totalCount:
                self.process.stdout.close()
                break

        # exe 文件运行结束
        self.ExErunning = False

        self.threadResult.emit("OK")

