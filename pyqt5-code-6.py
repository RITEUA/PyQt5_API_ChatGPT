import argparse
import os
import sys
from typing import Callable, Dict

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QSizePolicy,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import QSize, Qt
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

    def ask(self, question: str, update_callback: Callable):
        self._update_history(role="user", content=question)
        try:
            resp = openai.ChatCompletion.create(messages=self._history, **self._config)
        # TODO: handle openai.error's: Timeout, APIError, APIConnectionError etc.
        except Exception as e:
            update_callback(repr(e))
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
                    update_callback(resp_content)
            self._update_history(role="assistant", content=resp_content)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Налаштовуємо заголовок і розмір вікна програми
        self.setWindowTitle("PyQt5 + ChatGPT")
        self.setMinimumSize(QSize(500, 400))

        self.central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.chat = QTextBrowser()
        self.chat.setContentsMargins(0, 10, 0, 10)
        self.chat.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chat.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.chat.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.chat.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.chat.setOpenLinks(True)
        self.chat.setOpenExternalLinks(True)
        main_layout.addWidget(self.chat)

        # Створюємо і налаштовуємо текстове поле
        self.question = QLineEdit(self)  # Створення текстового поля
        self.question.returnPressed.connect(self.ask_chatgpt)
        main_layout.addWidget(self.question)

        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)
        self.question.setFocus()

        self.gpt = GPT()
        self.chat_text = ""
        self.separator = "\013" # <CR>
        self.gpt_format = f"{self.separator}<p><span style='color:#0f0;font-weight:700;'>GPT</span>: %s</p>"
        self.user_format = "<p><span style='color:#f00;font-weight:700;'>User</span>: %s</p>"

    # Генеруємо відповідь та показувати її в label
    def ask_chatgpt(self):
        question = self.question.text()
        if not len(question):
            return
        self.chat_text += self.user_format % question
        self.rerender_chat
        self.question.setText("")
        self.gpt.ask(question, lambda t: self.update_answer(t))
        self.chat_text = self.chat_text.replace(self.separator, "")

    def update_answer(self, text: str):
        history, *_ = self.chat_text.split(self.separator)
        self.chat_text = f"{history}{self.gpt_format % text}"
        self.rerender_chat()

    def rerender_chat(self):
        self.chat.setText(self.chat_text)
        current_scroll = self.chat.verticalScrollBar()
        if current_scroll.value() != current_scroll.maximum():
            current_scroll.setValue(current_scroll.maximum())
        QtWidgets.QApplication.processEvents()


# Запускаємо вікно програми
if __name__ == "__main__":
    init_key()
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
