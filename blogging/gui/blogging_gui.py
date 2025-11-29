# blogging/gui/blogging_gui.py
# Commit 2: add blog list panel (list + retrieve)
# Very basic & messy student style

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QApplication,
    QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt

from blogging.controller import Controller
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class BloggingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.setWindowTitle("SENG265 Blogging System")
        self.resize(900, 600)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        #
        # LOGIN BOX
        #
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

        #
        # BLOG LIST / RETRIEVE PANEL
        #
        blogs_box = QGroupBox("Blogs")
        blogs_layout = QHBoxLayout(blogs_box)

        self.blog_id_input = QLineEdit()
        self.blog_id_input.setPlaceholderText("enter blog id")

        self.btn_list_blogs = QPushButton("List Blogs")
        self.btn_retrieve_blog = QPushButton("Retrieve Blog")

        self.btn_list_blogs.clicked.connect(self.handle_list_blogs)
        self.btn_retrieve_blog.clicked.connect(self.handle_retrieve_blog)

        blogs_layout.addWidget(self.blog_id_input)
        blogs_layout.addWidget(self.btn_list_blogs)
        blogs_layout.addWidget(self.btn_retrieve_blog)

        layout.addWidget(blogs_box)

        #
        # OUTPUT BOX
        #
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        #
        # STATUS TEXT
        #
        self.status_label = QLabel("Not logged in.")
        layout.addWidget(self.status_label)

    #
    # LOGIN HANDLERS
    #
    def handle_login(self):
        u = self.user_edit.text().strip()
        p = self.pass_edit.text().strip()

        try:
            self.controller.login(u, p)
            self.status_label.setText(f"Logged in as {u}")
            self.login_btn.setEnabled(False)
            self.logout_btn.setEnabled(True)
        except DuplicateLoginException:
            self.status_label.setText("Already logged in")
        except InvalidLoginException:
            self.status_label.setText("Invalid login")

    def handle_logout(self):
        try:
            self.controller.logout()
            self.status_label.setText("Logged out.")
            self.login_btn.setEnabled(True)
            self.logout_btn.setEnabled(False)
        except InvalidLogoutException:
            self.status_label.setText("Not logged in.")

    #
    # BLOG PANEL HANDLERS
    #
    def handle_list_blogs(self):
        try:
            blogs = self.controller.list_blogs()
            out = ""
            for b in blogs:
                out += f"{b.id} | {b.title} | {b.name} | {b.email}\n"
            self.output.setText(out)
        except IllegalOperationException:
            self.output.setText("No blogs stored")

    def handle_retrieve_blog(self):
        bid_text = self.blog_id_input.text().strip()
        if not bid_text.isdigit():
            self.output.setText("Invalid blog id")
            return

        bid = int(bid_text)
        try:
            blog = self.controller.search_blog(bid)
            if blog is None:
                self.output.setText("Blog not found")
            else:
                self.output.setText(str(blog))
        except IllegalOperationException:
            self.output.setText("Error retrieving blog")
# blogging/gui/blogging_gui.py
# Commit 3: Add blog CRUD panel (create, update, delete, set/unset current)
# still messy but functional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QApplication,
    QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt

from blogging.controller import Controller
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException
from blogging.exception.illegal_access_exception import IllegalAccessException


class BloggingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.setWindowTitle("SENG265 Blogging System")
        self.resize(900, 750)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        #
        # LOGIN BOX
        #
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

        #
        # BLOG CRUD PANEL
        #
        crud_box = QGroupBox("Blog Management")
        crud = QVBoxLayout(crud_box)

        # row 1 — fields
        row = QHBoxLayout()
        self.field_id = QLineEdit()
        self.field_id.setPlaceholderText("id")
        self.field_title = QLineEdit()
        self.field_title.setPlaceholderText("title")
        self.field_name = QLineEdit()
        self.field_name.setPlaceholderText("name")
        self.field_email = QLineEdit()
        self.field_email.setPlaceholderText("email")

        row.addWidget(self.field_id)
        row.addWidget(self.field_title)
        row.addWidget(self.field_name)
        row.addWidget(self.field_email)
        crud.addLayout(row)

        # row 2 — operations
        ops = QHBoxLayout()
        self.btn_create = QPushButton("Create")
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Delete")
        self.btn_set = QPushButton("Set Current")
        self.btn_unset = QPushButton("Unset Current")

        self.btn_create.clicked.connect(self.handle_create_blog)
        self.btn_update.clicked.connect(self.handle_update_blog)
        self.btn_delete.clicked.connect(self.handle_delete_blog)
        self.btn_set.clicked.connect(self.handle_set_current)
        self.btn_unset.clicked.connect(self.handle_unset_current)

        ops.addWidget(self.btn_create)
        ops.addWidget(self.btn_update)
        ops.addWidget(self.btn_delete)
        ops.addWidget(self.btn_set)
        ops.addWidget(self.btn_unset)

        crud.addLayout(ops)

        layout.addWidget(crud_box)

        #
        # BLOG LIST / RETRIEVE PANEL
        #
        blogs_box = QGroupBox("Blogs")
        blogs_layout = QHBoxLayout(blogs_box)

        self.blog_id_input = QLineEdit()
        self.blog_id_input.setPlaceholderText("enter blog id")

        self.btn_list_blogs = QPushButton("List Blogs")
        self.btn_retrieve_blog = QPushButton("Retrieve Blog")

        self.btn_list_blogs.clicked.connect(self.handle_list_blogs)
        self.btn_retrieve_blog.clicked.connect(self.handle_retrieve_blog)

        blogs_layout.addWidget(self.blog_id_input)
        blogs_layout.addWidget(self.btn_list_blogs)
        blogs_layout.addWidget(self.btn_retrieve_blog)

        layout.addWidget(blogs_box)

        #
        # OUTPUT BOX
        #
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        #
        # STATUS TEXT
        #
        self.status_label = QLabel("Not logged in.")
        layout.addWidget(self.status_label)

    ####################################################################
    # LOGIN HANDLERS
    ####################################################################

    def handle_login(self):
        u = self.user_edit.text().strip()
        p = self.pass_edit.text().strip()

        try:
            self.controller.login(u, p)
            self.status_label.setText(f"Logged in as {u}")
            self.login_btn.setEnabled(False)
            self.logout_btn.setEnabled(True)
        except DuplicateLoginException:
            self.status_label.setText("Already logged in")
        except InvalidLoginException:
            self.status_label.setText("Invalid login")

    def handle_logout(self):
        try:
            self.controller.logout()
            self.status_label.setText("Logged out.")
            self.login_btn.setEnabled(True)
            self.logout_btn.setEnabled(False)
        except InvalidLogoutException:
            self.status_label.setText("Not logged in.")

    ####################################################################
    # BLOG CRUD HANDLERS
    ####################################################################

    def _read_blog_fields(self):
        try:
            bid = int(self.field_id.text().strip())
        except:
            return None
        title = self.field_title.text().strip()
        name = self.field_name.text().strip()
        email = self.field_email.text().strip()
        return (bid, title, name, email)

    def handle_create_blog(self):
        data = self._read_blog_fields()
        if not data:
            self.output.setText("Invalid input")
            return

        bid, title, name, email = data
        try:
            b = self.controller.create_blog(bid, title, name, email)
            self.output.setText(f"Created blog:\n{b}")
        except IllegalOperationException:
            self.output.setText("Duplicate blog ID")

    def handle_update_blog(self):
        data = self._read_blog_fields()
        if not data:
            self.output.setText("Invalid input")
            return

        bid, title, name, email = data
        try:
            ok = self.controller.update_blog(bid, bid, title, name, email)
            if ok:
                self.output.setText("Updated blog")
            else:
                self.output.setText("Update failed")
        except IllegalOperationException:
            self.output.setText("Blog not found")

    def handle_delete_blog(self):
        try:
            bid = int(self.field_id.text().strip())
        except:
            self.output.setText("Invalid id")
            return

        try:
            ok = self.controller.delete_blog(bid)
            if ok:
                self.output.setText("Deleted blog")
            else:
                self.output.setText("Delete failed")
        except IllegalOperationException:
            self.output.setText("Cannot delete current blog")

    def handle_set_current(self):
        try:
            bid = int(self.field_id.text().strip())
        except:
            self.output.setText("Invalid id")
            return

        try:
            ok = self.controller.set_current_blog(bid)
            if ok:
                self.output.setText(f"Set current blog to {bid}")
        except IllegalOperationException:
            self.output.setText("Blog not found")

    def handle_unset_current(self):
        try:
            ok = self.controller.unset_current_blog()
            if ok:
                self.output.setText("Unset current blog")
        except IllegalAccessException:
            self.output.setText("Not logged in")
        except NoCurrentBlogException:
            self.output.setText("No current blog selected")

    ####################################################################
    # BLOG RETRIEVE PANEL
    ####################################################################

    def handle_list_blogs(self):
        try:
            blogs = self.controller.list_blogs()
            out = ""
            for b in blogs:
                out += f"{b.id} | {b.title} | {b.name} | {b.email}\n"
            self.output.setText(out)
        except IllegalOperationException:
            self.output.setText("No blogs stored")

    def handle_retrieve_blog(self):
        bid_text = self.blog_id_input.text().strip()
        if not bid_text.isdigit():
            self.output.setText("Invalid blog id")
            return

        bid = int(bid_text)
        try:
            blog = self.controller.search_blog(bid)
            if blog is None:
                self.output.setText("Blog not found")
            else:
                self.output.setText(str(blog))
        except IllegalOperationException:
            self.output.setText("Error retrieving blog")

