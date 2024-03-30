from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap
from utils import get_resource_path

class AboutWidget(QWidget):

    send_result = Signal(str, str)

    def __init__(self, version="1.0", author="Uyukisan", description="串口调试工具"):
        super().__init__()

        self.__version = version
        self.__author = author
        self.__description = description
        self.init_ui()
        self.load_markdown_file(get_resource_path("./resources/README.md"))

    def init_ui(self):

        self.resize(200, 200)
        layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__author_label = QLabel("作者: " + self.author())
        self.__version_label = QLabel("版本: " + self.version())
        self.__description_label = QLabel("描述: " + self.description())
        self.__icon_label = QLabel()
        icon_pix = QPixmap(get_resource_path("./resources/serial.icns")).scaled(
            QSize(48, 48), Qt.KeepAspectRatio
        )
        self.__icon_label.setPixmap(icon_pix)

        self.__icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__author_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__version_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        top_layout.addWidget(self.__icon_label)
        top_layout.addWidget(self.__author_label)
        top_layout.addWidget(self.__version_label)
        top_layout.addWidget(self.__description_label)
        self.__text_browser = QTextBrowser()
        layout.addLayout(top_layout)
        layout.addWidget(self.__text_browser)

        self.setLayout(layout)

    def load_markdown_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                markdown_text = file.read()
                self.__text_browser.setMarkdown(markdown_text)
        except FileNotFoundError as e:
            self.send_result.emit("找不到README", "red")
            self.__text_browser.setMarkdown("加载帮助文档失败：找不到README文件")

    def version(self):
        return self.__version

    def set_version(self, version):

        self.__version = version
        self.__version_label.setText("版本: " + version)

    def author(self):
        return self.__author

    def set_author(self, author):

        self.__author = author
        self.__author_label.setText("作者: " + author)

    def author(self):

        return self.__author

    def description(self):

        return self.__description

    def set_description(self, description):

        self.__description = description
        self.__description_label.setText("描述: " + description)

    def set_logo(self, img_path):

        icon_pix = QPixmap(img_path).scaled(QSize(48, 48), Qt.KeepAspectRatio)
        self.__icon_label.setPixmap(icon_pix)
