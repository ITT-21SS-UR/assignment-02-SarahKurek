from PyQt5 import uic, Qt, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import pyqtSignal, QObject
import sys


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.win = uic.loadUi("calculator.ui", self)
        self.setup_buttons()
        self.input_text = ""
        self.numbers = ""
        self.calcModel = calcModel()
        self.setup_display()

    def setup_buttons(self):
        self.win.btn0.clicked.connect(
            lambda: self.calcModel.button_pressed("0"))
        self.win.btn1.clicked.connect(
            lambda: self.calcModel.button_pressed("1"))
        self.win.btn2.clicked.connect(
            lambda: self.calcModel.button_pressed("2"))
        self.win.btn3.clicked.connect(
            lambda: self.calcModel.button_pressed("3"))
        self.win.btn4.clicked.connect(
            lambda: self.calcModel.button_pressed("4"))
        self.win.btn5.clicked.connect(
            lambda: self.calcModel.button_pressed("5"))
        self.win.btn6.clicked.connect(
            lambda: self.calcModel.button_pressed("6"))
        self.win.btn7.clicked.connect(
            lambda: self.calcModel.button_pressed("7"))
        self.win.btn8.clicked.connect(
            lambda: self.calcModel.button_pressed("8"))
        self.win.btn9.clicked.connect(
            lambda: self.calcModel.button_pressed("9"))

        self.win.btnPoint.clicked.connect(
            lambda: self.calcModel.button_pressed("."))
        self.win.btnPlus.clicked.connect(
            lambda: self.calcModel.button_pressed("+"))
        self.win.btnMinus.clicked.connect(
            lambda: self.calcModel.button_pressed("-"))
        self.win.btnTimes.clicked.connect(
            lambda: self.calcModel.button_pressed("*"))
        self.win.btnDivide.clicked.connect(
            lambda: self.calcModel.button_pressed("/"))

        self.win.btnResult.clicked.connect(
            lambda: self.calcModel.button_pressed("="))
        self.win.btnDelete.clicked.connect(
            lambda: self.calcModel.button_pressed("del"))
        self.win.btnClear.clicked.connect(
            lambda: self.calcModel.button_pressed("clear"))

    def keyPressEvent(self, event):
        if self.calcModel.accepts(event.key()):
            self.calcModel.key_pressed(event)
            event.accept()
            return

        if event.key() == QtCore.Qt.Key_Return:
            self.win.btnResult.click()

        elif event.key() == QtCore.Qt.Key_Backspace:
            self.win.btnDelete.click()

        elif event.key() == QtCore.Qt.Key_Delete:
            self.win.btnClear.click()

        else:
            event.ignore()

    def setup_display(self):
        self.calcModel.data_changed.connect(
            lambda: self.win.lcdNumber.display(self.calcModel.display()))


class calcModel(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.text = ""
        self.formular = ""
        self.finished = False

    def is_operator(self, key_code):
        return (key_code == QtCore.Qt.Key_Plus) or \
            (key_code == QtCore.Qt.Key_Minus) or \
            (key_code == QtCore.Qt.Key_Asterisk) or \
            (key_code == QtCore.Qt.Key_Slash) or \
            (key_code == QtCore.Qt.Key_Delete) or \
            (key_code == QtCore.Qt.Key_Backspace) or \
            (key_code == QtCore.Qt.Key_Return)

    def is_digit(self, key_code):
        return key_code == QtCore.Qt.Key_0 or \
            key_code == QtCore.Qt.Key_1 or \
            key_code == QtCore.Qt.Key_2 or \
            key_code == QtCore.Qt.Key_3 or \
            key_code == QtCore.Qt.Key_4 or \
            key_code == QtCore.Qt.Key_5 or \
            key_code == QtCore.Qt.Key_6 or \
            key_code == QtCore.Qt.Key_7 or \
            key_code == QtCore.Qt.Key_8 or \
            key_code == QtCore.Qt.Key_9

    def is_period(self, key_code):
        return key_code == QtCore.Qt.Key_Period

    def to_key_code(self, text):
        if (text == "+"):
            return QtCore.Qt.Key_Plus

        if (text == "-"):
            return QtCore.Qt.Key_Minus

        if (text == "/"):
            return QtCore.Qt.Key_Slash

        if (text == "*"):
            return QtCore.Qt.Key_Asterisk

        if (text == "."):
            return QtCore.Qt.Key_Period

        if (text == "clear"):
            return QtCore.Qt.Key_Delete

        if (text == "del"):
            return QtCore.Qt.Key_Backspace

        if (text == "="):
            return QtCore.Qt.Key_Return

        return QtCore.Qt.Key_unknown

    def log_input(type):
        def log_decorator(function):
            def log_function(self, content):
                # sys.stdout.write("Following was entered: " + content + "\n")
                if type == 0:
                    sys.stdout.write(
                        "Following button was clicked: " + content + "\n")
                if type == 1:
                    sys.stdout.write(
                        "Following key was pressed: " + content.text() + "\n")

                function(self, content)

            return log_function
        return log_decorator

    @log_input(1)
    def key_pressed(self, event):
        if self.finished:
            self.clear()

        if not self.finished:
            if event.key() == int(QtCore.Qt.Key_Return):
                self.calculate()

            elif event.key() == int(QtCore.Qt.Key_Backspace):
                self.delete()

            elif event.key() == int(QtCore.Qt.Key_Delete):
                self.clear()

            else:
                self.handle_input(event.text())

    @log_input(0)
    def button_pressed(self, text):
        if self.finished:
            self.clear()

        if not self.finished:
            self.handle_input(text)

    def delete(self):
        if self.text:
            self.text = self.text[:-1]
            self.formular = self.formular[:-1]
            self.data_changed.emit()

    def clear(self):
        self.finished = False
        self.formular = ""
        self.text = ""
        self.data_changed.emit()

    def calculate(self):
        try:
            self.text = eval(self.formular)
        except SyntaxError:
            self.text = "Err"

        self.finished = True
        self.data_changed.emit()
        # sys.stdout.write("The result is: " + self.text + "\n")pppppppp

    def accepts(self, key_code):
        if self.is_digit(key_code):
            return True

        elif self.is_operator(key_code):
            return True

        elif self.is_period(key_code):
            return True

        return False

    def get_formular(self):
        return self.formular

    def display(self):
        if self.text == "":
            return "0"

        return self.text

    # @log_input()
    def handle_input(self, input):
        if not self.is_key_allowed(input):
            return

        if self.is_operator(self.to_key_code(input)):
            if input == "del":
                self.delete()

            elif input == "clear":
                self.clear()

            elif input == "=":
                self.calculate()

            else:
                self.text = ""

        else:
            self.text += input

        self.formular += input
        self.data_changed.emit()

    def is_key_allowed(self, key):
        key_code = self.to_key_code(key)

        if (self.is_operator(key_code)) \
            and (self.formular.endswith(key)
                 or (self.text == "")):
            return False

        if (self.is_period(key_code)) and ("." in self.text):
            return False

        return True


if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    win = Calculator()

    win.show()
    app.exec()
