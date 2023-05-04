# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import openai
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        MainWindow.setStyleSheet("#MainWindow {\n"
"    background-color: rgb(100, 105, 130);\n"
"}\n"
"\n"
"#question {\n"
"    background-color: rgb(120, 125, 150);\n"
"    border-radius: 10px;\n"
"    color: white;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"#go {\n"
"    background-color: rgb(0, 255, 175);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#go::hower {\n"
"    background-color: rgb(0, 225, 175);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#go::pressed {\n"
"    background-color: rgb(0, 205, 155);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#answer {\n"
"    color: white;\n"
"    font-size: 14px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.answer = QtWidgets.QLabel(self.centralwidget)
        self.answer.setGeometry(QtCore.QRect(10, 50, 480, 340))
        self.answer.setText("")
        self.answer.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.answer.setObjectName("answer")
        self.answer.setWordWrap(True)  # Додаємо авто перенесення рядків
        self.question = QtWidgets.QLineEdit(self.centralwidget)
        self.question.setGeometry(QtCore.QRect(10, 10, 400, 30))
        self.question.setObjectName("question")
        self.go = QtWidgets.QPushButton(self.centralwidget)
        self.go.setGeometry(QtCore.QRect(420, 10, 70, 30))
        self.go.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.go.setObjectName("go")
        self.go.clicked.connect(self.answer_chatgpt)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.go.setText(_translate("MainWindow", "GO!"))

    # Генеруємо відповідь та показувати її в label
    def answer_chatgpt(self):
        # Генерація відповідь від ChatGPT
        openai.api_key = "Введи сюди свій api_key"
        response = openai.Completion.create(
            engine="text-davinci-003",
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
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
