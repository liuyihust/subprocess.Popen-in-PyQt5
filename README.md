# Abstract
To show the usage of subprocess.Popen() in PyQt5.

主要为了记录 PyQt5 环境下，调用 subprocess.Popen() 时所踩过的两个坑。发现并解决这两个坑，花了我接近一天的时间！

# Problems

## Problem 01

### Description

原代码如下：
```python
# 子线程的 cmd 窗口属性
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
        
process = subprocess.Popen(cmd, startupinfo=startupinfo, shell=False, stdout=subprocess.PIPE)
```

在 PyCharm 中运行程序时，不会报任何错误；按 `pyinstaller -F main.py` 命令打包成 exe 文件时，也不会发生任何错误。但是，如果按 `pyinstaller -F -w main.py` 命令打包成 exe 文件时，程序运行到这个地方时，会导致闪退。

### Solution

在进行 Google 上找了很久，终于找到了答案，原来是 Popen 参数设置不完整所导致的。

需传入参数 `stdin=subprocess.PIPE, stderr=subprocess.STDOUT`。此外，还需令 `shell=True`，防止弹出一个 console。

```python
process = subprocess.Popen(cmd, startupinfo=startupinfo, shell=True,
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
```

## Problem 02

### Description

subprocessThread.py 文件中 `data = self.process.stdout.readline()` 这一行语句，主要功能是为了逐行读出 exe 文件的所有输出结果。

原来的代码是：

```python
while self.process.poll() is None:
    data = self.process.stdout.readline()
    # etc.
```

但当读完最后一行后，不仅会退出 while 循环，而且还会退出整个 run() 函数，导致后面的语句无法被执行到。

### Solution

在尝试了很多种方法后，都未尝见效。

最后只能选择避开这个问题，即加个判别条件，判断读取的数据是否是最后一行，如果是就跳出 while 循环，避免读取到最后一行数据的后一行。

很遗憾，这只是个缓兵之计，希望以后能找到解决办法吧。

