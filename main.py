if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    viewer = processDialog()
    viewer.show()

    sys.exit(app.exec_())
