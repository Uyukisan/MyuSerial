from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QSpinBox,
    QTextBrowser,
    QComboBox,
    QLabel,
)
from PySide6.QtCore import Qt, Signal

from serial import SerialManager


class MainWidget(QWidget):

    send_result = Signal(str, str)

    def __init__(self, serial_manager: SerialManager):
        super().__init__()

        self.serial_manager = serial_manager
        self.connect_params = None
        self.end_str_dict = {"\\r": "\r", "\\n": "\n", "#": "#", "@": "@", "None": ""}

        self.init_ui()

    def init_ui(self):

        self.resize(600, 600)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.connect_button = QPushButton("连接")
        self.connect_button.clicked.connect(self.connect_serial_port)

        self.disconnect_button = QPushButton("断开连接")
        self.disconnect_button.clicked.connect(self.disconnect_serial_port)

        connect_layout = QHBoxLayout()
        connect_layout.addWidget(self.connect_button)
        connect_layout.addWidget(self.disconnect_button)
        layout.addLayout(connect_layout)

        clear_button = QPushButton("清除打印")
        clear_button.clicked.connect(self.clear_text)

        self.receive_text_browser = QTextBrowser()
        layout.addWidget(self.receive_text_browser)

        layout.addWidget(clear_button)

        send_line_layout = QHBoxLayout()

        self.send_line_edit = QLineEdit()
        self.send_line_edit.setPlaceholderText("发送数据(Enter)")
        self.send_line_edit.textChanged[str].connect(self.update_send_str)
        self.send_line_edit.returnPressed.connect(self.send_data_manually)

        self.end_str_combo_box = QComboBox()
        self.end_str_combo_box.currentTextChanged.connect(self.update_send_str)
        self.end_str_combo_box.addItems(self.end_str_dict.keys())
        end_label = QLabel("结束符")

        send_line_layout.addWidget(self.send_line_edit)
        send_line_layout.addWidget(self.end_str_combo_box)
        send_line_layout.addWidget(end_label)
        layout.addLayout(send_line_layout)

        send_button = QPushButton("手动发送")
        send_button.clicked.connect(self.send_data_manually)
        layout.addWidget(send_button)

        sendInterLayout = QHBoxLayout()
        self.send_checkbox = QCheckBox("定时发送")
        self.send_checkbox.stateChanged.connect(self.toggle_send_timer)
        sendInterLayout.addWidget(self.send_checkbox)

        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setMinimum(1)
        self.interval_spinbox.setMaximum(10000)
        self.interval_spinbox.setValue(1000)
        sendInterLayout.addWidget(self.interval_spinbox)
        layout.addLayout(sendInterLayout)

        self.setLayout(layout)

    def update_send_str(self, text):

        # self.serial_manager.send_str = text
        self.serial_manager.send_str = (
            self.send_line_edit.text()
            + self.end_str_dict[self.end_str_combo_box.currentText()]
        )

    def send_data_manually(self):

        self.serial_manager.send_data()
        if self.serial_manager.send_success:
            self.send_result.emit("发送成功", "green")
        else:
            self.send_result.emit("发送失败", "red")
        self.send_line_edit.clear()

    def toggle_send_timer(self):
        if self.send_checkbox.isChecked():
            self.interval_spinbox.setDisabled(True)
            interval = self.interval_spinbox.value()
            self.serial_manager.start_send_timer(interval)
        else:
            self.interval_spinbox.setDisabled(False)
            self.serial_manager.stop_send_timer()

    def update_connect_params(self, params):
        self.connect_params = params

    def connect_serial_port(self):
        if self.connect_params == None:
            self.send_result.emit("连接失败(未确认连接设置)", "red")
        else:
            port_name, baud_rate, parity, stop_bits, data_bits, flow_control = (
                self.connect_params
            )
            if self.serial_manager.connect_serial_port(
                port_name, baud_rate, parity, stop_bits, data_bits, flow_control
            ):
                self.send_result.emit("串口连接成功:" + port_name, "green")
                self.connect_button.setDisabled(True)
            else:
                self.send_result.emit("串口连接失败:" + port_name, "red")

    def disconnect_serial_port(self):
        self.serial_manager.disconnect_serial_port()
        self.send_result.emit("已断开串口连接:" + self.current_port(), "green")
        self.connect_button.setDisabled(False)

    def current_port(self):
        return self.serial_manager.serial_port.portName()

    def current_text(self):
        return self.receive_text_browser.toPlainText()

    def clear_text(self):
        self.receive_text_browser.clear()

    def display_received_data(self, data):
        # self.receive_text_browser.insertPlainText(data)
        self.receive_text_browser.append(data.strip())
        self.receive_text_browser.ensureCursorVisible()
