import sys
from blogging.configuration import Configuration
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLabel, QLineEdit
from blogging.gui.login_gui import LoginGUI
from blogging.controller import Controller


class BloggingGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # set autosave to True to ensure persistence is working
        self.configuration = Configuration()
        self.configuration.__class__.autosave = True
        # Continue here with your code!

        self.setWindowTitle("Gabriel and Michael's Blogging App")
        self.setMaximumSize(1920, 1080)

        middle = QWidget()
        self.setCentralWidget(middle)
        self.layout = QVBoxLayout()
        middle.setLayout(self.layout)

        self.controller = Controller()
        self.current_user = None

        self.login_widget = LoginGUI(self.controller)
        self.login_widget.setFixedSize(200,200)
        self.layout.addWidget(self.login_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.login_widget.login_success.connect(self.when_login_successful)
        self.login_widget.login_fail.connect(self.when_login_failed)

    #Successful Login Prompt
    def when_login_successful(self, username):
        self.current_user = username
        user_login_widget = QLabel(f"Logged in as {self.current_user}")
        self.layout.addWidget(user_login_widget)
        self.layout.addWidget(user_login_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

    #Failed Login Prompt
    def when_login_failed(self):
        user_login_fail_widget = QLabel(f"Failed to login. Invalid username or password.")
        self.layout.addWidget(user_login_fail_widget)
        self.layout.addWidget(user_login_fail_widget, alignment=Qt.AlignmentFlag.AlignHCenter)


def main():
    app = QApplication(sys.argv)
    window = BloggingGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
