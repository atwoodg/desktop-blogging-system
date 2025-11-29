# blogging/gui/blogging_gui.py
# Commit 1: minimal window + login box only

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QApplication,
    QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt

from blogging.controller import Controller
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException


class BloggingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.setWindowTitle("SENG265 Blogging System")
        self.resize(800, 300)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # --------------------------
        # LOGIN BOX (Commit 1 only)
        # --------------------------
        login_box = QGroupBox("Login")
        login_layout = QHBoxLayout(login_box)

        self.user_edit = QLineEdit()
        self.user_edit.setPlaceholderText("username")

        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_edit.setPlaceholderText("password")

        self.login_btn = QPushButton("Login")
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setEnabled(False)

        self.login_btn.clicked.connect(self.handle_login)
        self.logout_btn.clicked.connect(self.handle_logout)

        login_layout.addWidget(QLabel("User:"))
        login_layout.addWidget(self.user_edit)
        login_layout.addWidget(QLabel("Pass:"))
        login_layout.addWidget(self.pass_edit)
        login_layout.addWidget(self.login_btn)
        login_layout.addWidget(self.logout_btn)

        layout.addWidget(login_box)

        # bottom status
        self.status_label = QLabel("Not logged in.")
        layout.addWidget(self.status_label)

    # --------------------------
    # Login handlers
    # --------------------------
    def handle_login(self):
        u = self.user_edit.text().strip()
        p = self.pass_edit.text().strip()

        try:
            self.controller.login(u, p)
            self.status_label.setText(f"Logged in as {u}")
            self.login_btn.setEnabled(False)
            self.logout_btn.setEnabled(True)
        except DuplicateLoginException:
            self.status_label.setText("Already logged in.")
        except InvalidLoginException:
            self.status_label.setText("Invalid credentials.")

    def handle_logout(self):
        try:
            self.controller.logout()
            self.status_label.setText("Logged out.")
            self.login_btn.setEnabled(True)
            self.logout_btn.setEnabled(False)
        except InvalidLogoutException:
            self.status_label.setText("Not logged in.")
