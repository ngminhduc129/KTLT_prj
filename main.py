# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import QTextCodec
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont


def main():
    app = QApplication(sys.argv)
    QTextCodec.setCodecForLocale(QTextCodec.codecForName("UTF-8"))
    app.setStyle("Fusion")
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    from UI.main_window import MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    