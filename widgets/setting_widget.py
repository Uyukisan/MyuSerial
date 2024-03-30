from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QComboBox,
    QPushButton,
)
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import Qt, Signal


class SettingWidget(QWidget):

    confirm_signal = Signal(int, object)

    def __init__(self):
        super().__init__()

        self.stop_bit_dict = {"1": "OneStop", "1.5": "OneAndHalfStop", "2": "TwoStop"}
        self.data_bit_dict = {"5": "Data5", "6": "Data6", "7": "Data7", "8": "Data8"}
        self.parity_dict = {
            "None": "NoParity",
            "Even": "EvenParity",
            "Odd": "OddParity",
            "Mark": "MarkParity",
            "Space": "SpaceParity",
        }
        self.flow_dict = {
            "NoFlow": "NoFlowControl",
            "Hardware": "HardwareControl",
            "Software": "SoftwareControl",
        }
        self.init_ui()

    def init_ui(self):

        # self.resize(400, 300)
        # self.setContentsMargins(64, 64, 80, 80)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        port_layout = QHBoxLayout()
        port_label = QLabel("串口:")
        port_layout.addWidget(port_label)
        self.port_combo_box = QComboBox()
        self.refresh_ports()
        port_layout.addWidget(self.port_combo_box)

        baud_rate_layout = QHBoxLayout()
        baud_rate_label = QLabel("波特率:")
        baud_rate_layout.addWidget(baud_rate_label)
        self.baud_rate_combo_box = QComboBox()
        self.baud_rate_combo_box.addItems(["9600", "19200", "38400", "57600", "115200"])
        baud_rate_layout.addWidget(self.baud_rate_combo_box)

        parity_layout = QHBoxLayout()
        parity_label = QLabel("校验位:")
        parity_layout.addWidget(parity_label)
        self.parity_combo_box = QComboBox()
        self.parity_combo_box.addItems(self.parity_dict.keys())
        parity_layout.addWidget(self.parity_combo_box)

        stop_bits_layout = QHBoxLayout()
        stop_bits_label = QLabel("停止位:")
        stop_bits_layout.addWidget(stop_bits_label)
        self.stop_bits_combo_box = QComboBox()
        self.stop_bits_combo_box.addItems(self.stop_bit_dict.keys())
        stop_bits_layout.addWidget(self.stop_bits_combo_box)

        data_bits_layout = QHBoxLayout()
        data_bits_label = QLabel("数据位:")
        data_bits_layout.addWidget(data_bits_label)
        self.data_bits_combo_box = QComboBox()
        self.data_bits_combo_box.addItems(self.data_bit_dict.keys())
        data_bits_layout.addWidget(self.data_bits_combo_box)

        flow_control_layout = QHBoxLayout()
        flow_control_label = QLabel("流控制")
        flow_control_layout.addWidget(flow_control_label)
        self.flow_control_combo_box = QComboBox()
        self.flow_control_combo_box.addItems(self.flow_dict.keys())
        flow_control_layout.addWidget(self.flow_control_combo_box)

        confirm_button = QPushButton("确认")
        confirm_button.clicked.connect(self.__confirm_setting)

        layout.addLayout(port_layout)
        layout.addLayout(baud_rate_layout)
        layout.addLayout(parity_layout)
        layout.addLayout(stop_bits_layout)
        layout.addLayout(data_bits_layout)
        layout.addLayout(flow_control_layout)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def refresh_ports(self):

        port_infos = QSerialPortInfo.availablePorts()
        for port_info in port_infos:
            self.port_combo_box.addItem(port_info.portName())

    def get_setting(self):
        port_name = self.port_combo_box.currentText()
        baud_rate = int(self.baud_rate_combo_box.currentText())
        parity = getattr(
            QSerialPort, self.parity_dict[self.parity_combo_box.currentText()]
        )
        stop_bits = getattr(
            QSerialPort, self.stop_bit_dict[self.stop_bits_combo_box.currentText()]
        )
        data_bits = getattr(
            QSerialPort, self.data_bit_dict[self.data_bits_combo_box.currentText()]
        )
        flow_control = getattr(
            QSerialPort, self.flow_dict[self.flow_control_combo_box.currentText()]
        )
        return (port_name, baud_rate, parity, stop_bits, data_bits, flow_control)

    def __confirm_setting(self):

        self.confirm_signal.emit(1, self.get_setting())
