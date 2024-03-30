from PySide6.QtSerialPort import QSerialPort
from PySide6.QtCore import QTimer

class SerialManager:

    def __init__(self, receive_callback, send_str="Hello, Serial", silence=False):
        self.serial_port = QSerialPort()
        self.receive_callback = receive_callback
        self.send_str = send_str
        self.serial_port.readyRead.connect(self.receive_data)
        self.send_timer = QTimer()
        self.send_timer.timeout.connect(self.send_data)
        self.send_success = False
        self.keep_silence = silence
        self.received_data = ""

    def connect_serial_port(
        self, port_name, baud_rate, parity, stop_bits, data_bits, flow_control
    ):
        self.serial_port.setPortName(port_name)
        self.serial_port.setBaudRate(baud_rate)
        self.serial_port.setParity(parity)
        self.serial_port.setStopBits(stop_bits)
        self.serial_port.setDataBits(data_bits)
        self.serial_port.setFlowControl(flow_control)
        if self.serial_port.open(QSerialPort.ReadWrite):
            return True
        else:
            return False

    def disconnect_serial_port(self):
        if self.serial_port.isOpen():
            self.serial_port.close()

    def send_data(self, data: str = ""):
        if data == "":
            data = self.send_str
        if self.keep_silence != True:
            # print("SerialManager::send str: %s" % data)
            pass
        if self.serial_port.write(data.encode()) != -1:
            self.send_success = True
        else:
            self.send_success = False

    def start_send_timer(self, interval):
        self.send_timer.start(interval)

    def stop_send_timer(self):
        self.send_timer.stop()

    def receive_data(self):
        self.received_data += self.serial_port.readAll().data().decode()
        if "\n" in self.received_data:
            lines = self.received_data.split("\n")
            for line in lines[:-1]:
                self.receive_callback(line)
            self.received_data = lines[-1] # 最后一行可能未发送完成
