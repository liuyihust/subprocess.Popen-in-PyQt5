if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from processDialog import ProcessDialog

    app = QApplication(sys.argv)
    viewer = ProcessDialog()
    viewer.show()

    sys.exit(app.exec_())
