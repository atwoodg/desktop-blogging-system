import sys
from blogging.configuration import Configuration
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget

from blogging.controller import Controller

class LoginGUI(QWidget):
    login_success = pyqtSignal(str)
    login_fail = pyqtSignal()

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.username = QLineEdit()
        self.username.setPlaceholderText("USERNAME")
        layout.addWidget(QLabel("Enter Username:"))
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("PASSWORD")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Enter Password:"))
        layout.addWidget(self.password)

        self.login = QPushButton("LOGIN")
        layout.addWidget(self.login)

        self.login.clicked.connect(self.user_login)

    def user_login(self):
        username = self.username.text()
        password = self.password.text()

        try:
            if self.controller.login(username, password):
                self.login_success.emit(username)
        except Exception:
                self.login_fail.emit()