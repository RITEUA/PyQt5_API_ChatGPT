import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Налаштовуємо заголовок і розмір вікна програми
        self.setWindowTitle("Кнопка")
        self.setMinimumSize(QSize(200, 150))

        # Створюємо і налаштовуємо кнопку
        self.button = QPushButton("КЛАЦНИ", self)
        self.button.resize(180, 130)
        self.button.move(10, 10)
        self.button.clicked.connect(self.click_button)

    def click_button(self):
        self.button.setText("ДЯКУЮ")


# Запускаємо вікно програми
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
