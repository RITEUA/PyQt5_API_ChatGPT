import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Налаштовуємо заголовок і розмір вікна програми
        self.setWindowTitle("Текстова мітка")
        self.setMinimumSize(QSize(200, 150))

        # Створюємо і налаштовуємо кнопку
        self.button_add = QPushButton("+", self)
        self.button_add.resize(180, 40)
        self.button_add.move(10, 10)
        self.button_add.clicked.connect(self.add_one)

        self.n = 0  # Змінна, яка потрібна для зміни тексту в мітці на більше число

        # Створюємо і налаштовуємо текстову мітку
        self.label = QLabel(str(self.n), self)  # Створення мітки
        self.label.resize(180, 80)  # Зміна розміру
        self.label.move(10, 60)  # Зміна розташування
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # Виставлення тексту по центру

    # Змінюємо текст текстової мітки, на число, яке з кожним натисканням кнопки: більше на 1
    def add_one(self):
        self.n += 1
        self.label.setText(str(self.n))


# Запускаємо вікно програми
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
