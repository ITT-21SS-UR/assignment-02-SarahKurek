from PyQt5 import uic, Qt, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import pyqtSignal, QObject
from enum import Enum
import sys


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.win = uic.loadUi("calculator.ui", self)
        self.calc_model = CalcModel()
        self.setup_ui()

    def setup_buttons(self):
        self.win.btn0.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_0))
        self.win.btn1.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_1))
        self.win.btn2.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_2))
        self.win.btn3.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_3))
        self.win.btn4.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_4))
        self.win.btn5.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_5))
        self.win.btn6.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_6))
        self.win.btn7.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_7))
        self.win.btn8.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_8))
        self.win.btn9.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_9))

        self.win.btnPoint.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Period))
        self.win.btnPlus.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Plus))
        self.win.btnMinus.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Minus))
        self.win.btnTimes.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Asterisk))
        self.win.btnDivide.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Slash))

        self.win.btnResult.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Return))
        self.win.btnDelete.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Backspace))
        self.win.btnClear.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Delete))

    def keyPressEvent(self, event):
        if self.calc_model.can_handle_key(event.key()):
            self.calc_model.key_pressed(event.key())
            event.accept()

        else:
            event.ignore()

    def setup_ui(self):
        # label to display the current operator (initialized empty).
        self.win.lblOperator.setText("")
        self.setup_buttons()

        # lcd panel with 15 digits to display the current number.
        self.calc_model.model_changed.connect(
            lambda: self.win.lcdNumber.display(self.calc_model.get_display_text()))
        self.calc_model.model_changed.connect(
            lambda: self.win.lblOperator.setText(self.calc_model.get_operator()))


class CalcModel(QObject):
    # input source (button, key, result) for proper logging
    class LoggingEntity(Enum):
        BUTTON = 0
        KEY = 1
        RESULT = 2

    model_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.text = ""  # current digits
        self.formula = ""  # current formula with operators
        self.finished = False  # indicates a finished calculation

    @staticmethod
    def is_operator(key_code):
        return key_code == QtCore.Qt.Key_Plus \
            or key_code == QtCore.Qt.Key_Minus \
            or key_code == QtCore.Qt.Key_Asterisk \
            or key_code == QtCore.Qt.Key_Slash \
            or key_code == QtCore.Qt.Key_Delete \
            or key_code == QtCore.Qt.Key_Backspace \
            or key_code == QtCore.Qt.Key_Return \
            or key_code == QtCore.Qt.Key_Enter

    @staticmethod
    def is_digit(key_code):
        return key_code == QtCore.Qt.Key_0 \
            or key_code == QtCore.Qt.Key_1 \
            or key_code == QtCore.Qt.Key_2 \
            or key_code == QtCore.Qt.Key_3 \
            or key_code == QtCore.Qt.Key_4 \
            or key_code == QtCore.Qt.Key_5 \
            or key_code == QtCore.Qt.Key_6 \
            or key_code == QtCore.Qt.Key_7 \
            or key_code == QtCore.Qt.Key_8 \
            or key_code == QtCore.Qt.Key_9

    def is_period(key_code):
        return key_code == QtCore.Qt.Key_Period or key_code == QtCore.Qt.Key_Comma

    @staticmethod
    def key_code_to_text(key_code):
        if key_code == QtCore.Qt.Key_0:
            return "0"

        if key_code == QtCore.Qt.Key_1:
            return "1"

        if key_code == QtCore.Qt.Key_2:
            return "2"

        if key_code == QtCore.Qt.Key_3:
            return "3"

        if key_code == QtCore.Qt.Key_4:
            return "4"

        if key_code == QtCore.Qt.Key_5:
            return "5"

        if key_code == QtCore.Qt.Key_6:
            return "6"

        if key_code == QtCore.Qt.Key_7:
            return "7"

        if key_code == QtCore.Qt.Key_8:
            return "8"

        if key_code == QtCore.Qt.Key_9:
            return "9"

        if key_code == QtCore.Qt.Key_Plus:
            return "+"

        if key_code == QtCore.Qt.Key_Minus:
            return "-"

        if key_code == QtCore.Qt.Key_Asterisk:
            return "*"

        if key_code == QtCore.Qt.Key_Slash:
            return "/"

        if key_code == QtCore.Qt.Key_Backspace:
            return "delete"

        if key_code == QtCore.Qt.Key_Delete:
            return "clear"

        if key_code == QtCore.Qt.Key_Return or key_code == QtCore.Qt.Key_Enter:
            return "="

        if CalcModel.is_period(key_code):
            return "."

    @staticmethod
    def text_to_key_code(text):
        if text == "+":
            return QtCore.Qt.Key_Plus

        if text == "-":
            return QtCore.Qt.Key_Minus

        if text == "*":
            return QtCore.Qt.Key_Asterisk

        if text == "/":
            return QtCore.Qt.Key_Slash

    def log_input(type):
        def log_decorator(function):
            def log_function(self, to_be_logged):
                if type == CalcModel.LoggingEntity.BUTTON:
                    sys.stdout.write(
                        "Following button was clicked: " + CalcModel.key_code_to_text(to_be_logged) + "\n")

                elif type == CalcModel.LoggingEntity.KEY:
                    sys.stdout.write(
                        "Following key was pressed: " + CalcModel.key_code_to_text(to_be_logged) + "\n")

                elif type == CalcModel.LoggingEntity.RESULT:
                    sys.stdout.write(
                        "Following result was evaluated: " + str(to_be_logged) + "\n")

                function(self, to_be_logged)

            return log_function
        return log_decorator

    @log_input(LoggingEntity.KEY)
    def key_pressed(self, key_code):
        if self.finished:
            self.clear()

        self.handle_input(key_code)

    @log_input(LoggingEntity.BUTTON)
    def button_pressed(self, key_code):
        if self.finished:
            self.clear()

        self.handle_input(key_code)

    @log_input(LoggingEntity.RESULT)
    def on_result_evaluated(self, result):
        self.text = result
        self.finished = True
        self.model_changed.emit()

    def delete(self):
        if self.text:
            self.text = self.text[:-1]
            self.model_changed.emit()

    def clear(self):
        self.finished = False
        self.formula = ""
        self.text = ""
        self.model_changed.emit()

    def calculate(self):
        try:
            if self.formula:
                self.on_result_evaluated(eval(self.formula))
        except SyntaxError:
            self.text = "ERR"

    def can_handle_key(self, key_code):
        if CalcModel.is_digit(key_code) \
            or CalcModel.is_operator(key_code) \
                or CalcModel.is_period(key_code):
            return True

        return False

    def get_display_text(self):
        if not self.text:
            return "0"

        return self.text

    def get_operator(self):
        if not self.formula:
            return ""

        if self.finished:
            return "="

        return self.formula[-1]

    def handle_input(self, key_code):
        # if key is not alllowed the input is ignored
        if not self.is_key_allowed(key_code):
            return

        # the key code is converted to its text representation
        key_text = CalcModel.key_code_to_text(key_code)

        if CalcModel.is_operator(key_code):
            if key_code == QtCore.Qt.Key_Delete:
                self.clear()

            elif key_code == QtCore.Qt.Key_Backspace:
                self.delete()

            # before calculation the text is appended to the formula
            elif key_code == QtCore.Qt.Key_Return or key_code == QtCore.Qt.Key_Enter:
                self.formula += self.text
                self.calculate()

            # this effectively changes the current operator
            elif self.formula and not self.text:
                self.formula = self.formula[:-1] + key_text

            elif self.text:
                self.formula += self.text + key_text
                self.text = ""

        else:
            self.text += key_text

        self.model_changed.emit()

    def is_key_allowed(self, key_code):
        if CalcModel.is_period(key_code) and ("." in self.text):
            return False

        return True


if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    win = Calculator()

    win.show()
    app.exec()
