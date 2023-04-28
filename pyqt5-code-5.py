import argparse
import os
import sys
from typing import Callable, Dict

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


class GPT:
    def __init__(self) -> None:
        self._history = []
        self._config = {
            "model": "gpt-3.5-turbo",
            "stream": True,
            "temperature": 0.7,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }

    def _update_history(self, **kwargs):
        self._history.append(kwargs)

    def ask(self, question: str, update_label_callback: Callable):
        self._update_history(role="user", content=question)
        try:
            resp = openai.ChatCompletion.create(messages=self._history, **self._config)
        # TODO: handle openai.error's: Timeout, APIError, APIConnectionError etc.
        except Exception as e:
            update_label_callback(repr(e))
        else:
            resp_content = ""
            delta_list = list()
            for chunk in resp:
                if (
                    not isinstance(chunk, Dict)
                    or not (choices := chunk.get("choices"))
                    or not len(choices)
                ):
                    continue

                if delta := choices.pop().get("delta"):
                    delta_list.append(delta)
                    resp_content = "".join([m.get("content", "") for m in delta_list])
                    update_label_callback(resp_content)
            self._update_history(role="assistant", content=resp_content)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gpt = GPT()

        # Налаштовуємо заголовок і розмір вікна програми
        self.setWindowTitle("PyQt5 + ChatGPT")
        self.setMinimumSize(QSize(500, 400))

        # Створюємо і налаштовуємо текстове поле
        self.question = QLineEdit(self)  # Створення текстового поля
        self.question.resize(400, 30)  # Зміна розміру
        self.question.move(10, 10)  # Зміна розташування
        self.question.returnPressed.connect(self.answer_chatgpt)

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

    def update_label(self, msg=""):
        self.answer.setText(msg)
        QtWidgets.QApplication.processEvents()

    # Генеруємо відповідь та показувати її в label
    def answer_chatgpt(self):
        question = self.question.text()
        if not len(question):
            return
        self.question.setText("")
        self.update_label()
        self.gpt.ask(question, self.update_label)


# Запускаємо вікно програми
if __name__ == "__main__":
    init_key()
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
