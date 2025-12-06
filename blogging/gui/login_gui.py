# blogging/gui/login_gui.py
# simple login widget for the blogging system

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)

from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException


class LoginGUI(QWidget):
    # will tell the main window when login worked or failed
    login_success = pyqtSignal(str)
    login_fail = pyqtSignal()

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Login to Blogging System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # username
        self.user_edit = QLineEdit()
        self.user_edit.setPlaceholderText("username")
        main_layout.addWidget(self.user_edit)

        # password
        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText("password")
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        main_layout.addWidget(self.pass_edit)

        # small message label
        self.msg_label = QLabel("")
        main_layout.addWidget(self.msg_label)

        # login button centered
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self._do_login)
        btn_row.addWidget(self.login_btn)
        btn_row.addStretch()
        main_layout.addLayout(btn_row)

        self.setLayout(main_layout)

    def _do_login(self):
        username = self.user_edit.text().strip()
        password = self.pass_edit.text()

        if not username or not password:
            self.msg_label.setText("Please type username and password.")
            self.login_fail.emit()
            return

        try:
            ok = self.controller.login(username, password)
            if ok:
                self.msg_label.setText("")
                self.login_success.emit(username)
        except (InvalidLoginException, DuplicateLoginException):
            # credentials wrong or already logged in
            self.msg_label.setText("Invalid username/password or already logged in.")
            self.login_fail.emit()
        except Exception as e:
            # anything unexpected
            self.msg_label.setText(f"Error: {e}")
            self.login_fail.emit()
