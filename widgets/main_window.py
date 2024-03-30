from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QFileDialog,
)
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtCore import QTextStream, QIODevice, QFile, QStringConverter

from serial import SerialManager
from widgets import SettingWidget, MainWidget, AboutWidget
from utils import get_resource_path


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MyuSerial")
        self.resize(600, 600)

        self.serial_manager = SerialManager(self.receive_callback, "")

        self.stacked_widget = QStackedWidget()
        self.main_widget = MainWidget(self.serial_manager)
        self.setting_widget = SettingWidget()
        self.about_widget = AboutWidget()
        self.about_widget.set_version("1.0.0")
        self.about_widget.set_logo(get_resource_path("./resources/serial.png"))

        self.stacked_widget.addWidget(self.setting_widget)
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.about_widget)

        self.setting_widget.confirm_signal.connect(self.set_current_widget)
        self.main_widget.send_result.connect(self.show_status)
        self.about_widget.send_result.connect(self.show_status)

        self.setCentralWidget(self.stacked_widget)

        self.init_ui()

    def init_ui(self):

        self.statusBar = self.statusBar()
        main_action = QAction("主页", self)
        main_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.main_widget)
        )
        main_action.setShortcut("Ctrl+1")

        settings_action = QAction("设置", self)
        settings_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.setting_widget)
        )
        settings_action.setShortcut("Ctrl+2")

        about_action = QAction("关于", self)
        about_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.about_widget)
        )
        about_action.setShortcut("Ctrl+3")

        save_action = QAction("保存打印数据", self)
        save_action.triggered.connect(self.save_received_data)
        save_action.setShortcut("Ctrl+S")

        menubar = self.menuBar()
        page_menu = menubar.addMenu("页面")
        page_menu.addAction(main_action)
        page_menu.addAction(settings_action)
        page_menu.addAction(about_action)
        file_menu = menubar.addMenu("文件")
        file_menu.addAction(save_action)

    def closeEvent(self, event: QCloseEvent) -> None:

        reply = QMessageBox.question(
            self,
            "关闭程序",
            "你确认关闭?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            # print("Serial::quit app")
            self.serial_manager.disconnect_serial_port()
            event.accept()
        else:
            # print("Serial::cancel quit")
            event.ignore()

    def show_status(self, msg, color):
        self.statusBar.showMessage(msg)
        self.statusBar.setStyleSheet(f"color: {color};")

    def set_current_widget(self, index, params):
        self.stacked_widget.setCurrentIndex(index)
        if self.main_widget.isHidden() != True:
            self.main_widget.update_connect_params(params)

    def receive_callback(self, data):
        self.main_widget.display_received_data(data)

    def save_received_data(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存接收数据", "", "Text Files (*.txt)"
        )
        if filename:
            file = QFile(filename)
            if file.open(QIODevice.WriteOnly | QIODevice.Text):
                text_stream = QTextStream(file)
                text_stream.setEncoding(QStringConverter.Encoding.Utf8)
                text_stream << self.main_widget.current_text()
                file.close()
