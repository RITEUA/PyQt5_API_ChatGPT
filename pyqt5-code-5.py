import argparse
import os
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QSize
import openai


DEFAULT_API_KEY_PATH = ...


def read_key(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        pass


def init_key():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="api key path (optional)")
    parser.add_argument("-k", "--key", help="api key (optional)")
    args = {k: str(v) for k, v in vars(parser.parse_args()).items() if v}
    if (
        (api_key := args.get("key"))
        or (api_key := read_key(args.get("path", DEFAULT_API_KEY_PATH)))
        or (api_key := os.getenv("OPENAI_API_KEY"))
    ):
        openai.api_key = api_key
    else:
        parser.print_help()
        sys.exit("\nProvide API Key")


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
        self.answer.setAlignment(
            QtCore.Qt.AlignTop
        )  # Вирівнюємо текст по верхньому лівому краю
        self.answer.setWordWrap(True)  # Додаємо авто перенесення рядків

    # Генеруємо відповідь та показувати її в label
    def answer_chatgpt(self):
        # Генерація відповідь від ChatGPT
        response = openai.Completion.create(
            engine="text-davinci-003",  # Виберіть бажаний "engine" (davinci-codex, codex-babbage-001, ... )
            prompt=self.question.text(),
            max_tokens=1024,
            temperature=0.7,
            n=1,
            format="text",
        )
        self.answer.setText(
            response.choices[0].text[2:]
        )  # Змінюємо текст мітки на відповідь від ChatGPT


# Запускаємо вікно програми
if __name__ == "__main__":
    init_key()
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
