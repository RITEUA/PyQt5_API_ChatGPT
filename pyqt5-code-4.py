import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QSize
import openai


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Налаштовуємо заголовок і розмір вікна програми
        self.setWindowTitle("PyQt5 + ChatGPT")
        self.setMinimumSize(QSize(500, 400))

        # Створюємо і налаштовуємо текстове поле
        self.question = QLineEdit(self)  # Створення текстового поля
        self.question.resize(400, 30)  # Зміна розміру
        self.question.move(10, 10)  # Зміна розташування

        # Створюємо і налаштовуємо кнопку
        self.go = QPushButton("GO", self)  # Створення кнопки
        self.go.resize(70, 30)  # Зміна розміру
        self.go.move(420, 10)  # Зміна розташування
        self.go.clicked.connect(self.answer_chatgpt)

        # Створюємо і налаштовуємо текстову мітку
        self.answer = QLabel(self)  # Створення текстової мітки
        self.answer.resize(480, 340)  # Зміна розміру
        self.answer.move(10, 50)  # Зміна розташування
        self.answer.setAlignment(QtCore.Qt.AlignTop)  # Вирівнюємо текст по верхньому лівому краю
        self.answer.setWordWrap(True)  # Додаємо авто перенесення рядків

    # Генеруємо відповідь та показувати її в label
    def answer_chatgpt(self):
        # Генерація відповідь від ChatGPT
        openai.api_key = "Введи сюди свій api_key"  # Замініть YOUR_API_KEY_HERE на свій API ключ
        response = openai.Completion.create(
            engine="text-davinci-003",  # Виберіть бажаний "engine" (davinci-codex, codex-babbage-001, ... )
            prompt=self.question.text(),
            max_tokens=1024,
            temperature=0.7,
            n=1,
            format="text",
        )
        self.answer.setText(response.choices[0].text[2:])  # Змінюємо текст мітки на відповідь від ChatGPT


# Запускаємо вікно програми
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
