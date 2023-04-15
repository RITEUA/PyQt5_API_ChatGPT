import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Налаштовуємо заголовок і розмір вікна програми
        self.setWindowTitle("Текстове поле")
        self.setMinimumSize(QSize(200, 150))

        # Створюємо і налаштовуємо текстове поле
        self.lineedit = QLineEdit(self)  # Створення текстового поля
        self.lineedit.resize(180, 30)  # Зміна розміру
        self.lineedit.move(10, 10)  # Зміна розташування

        # Створюємо і налаштовуємо кнопку
        self.button_change = QPushButton("Змінити текст мітки", self)
        self.button_change.resize(180, 40)
        self.button_change.move(10, 50)
        self.button_change.clicked.connect(self.change_text)

        # Створюємо і налаштовуємо текстову мітку
        self.label = QLabel("Введи і клацни", self)
        self.label.resize(180, 50)
        self.label.move(10, 95)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

    # Змінюємо текст мітки, на текст, який буде введено у текстове поле
    def change_text(self):
        self.label.setText(self.lineedit.text())


# Запускаємо вікно програми
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
