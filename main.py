import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from widgets import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MyuSerial")
    app.setApplicationDisplayName("MyuSerial")
    app.setWindowIcon(QIcon("./resources/serial.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
