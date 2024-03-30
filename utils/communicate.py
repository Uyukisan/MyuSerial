from PySide6.QtCore import Signal, QObject


class Communicator(QObject):

    __signal = Signal(object)
    __name = ""

    def __init__(self):
        super().__init__()

        print("Communicator init..")

    def send(self, name, message):

        print(message)
        self.__name = name
        self.__signal.emit(message)

    def connect(self, slot: object, *args):

        self.__signal.connect(slot)

    def get_name(self):

        return self.__name
