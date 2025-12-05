from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTableView, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import pyqtSignal
from blogging.blog import Blog

class Dashboard(QWidget):

    clicked_logout = pyqtSignal()

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.dash = QWidget()
        dash_layout = QVBoxLayout()
        self.dash.setLayout(dash_layout)

        dash_layout.addWidget(QLabel("BLOG DASHBOARD"))

        #Search for blog operations
        search_blog_button = QPushButton("Search For Blog")
        dash_layout.addWidget(search_blog_button)
        search_blog_button.clicked.connect(self.open_search_blog)

        #Create new blog operations
        create_blog_button = QPushButton("Create New Blog")
        dash_layout.addWidget(create_blog_button)
        create_blog_button.clicked.connect(self.open_create_blog)

        #Retrieve blog operations
        retrieve_blog_button = QPushButton("Retrieve Blog")
        dash_layout.addWidget(retrieve_blog_button)
        retrieve_blog_button.clicked.connect(self.open_retrieve_blog)

        #Update blog operations
        update_blog_button = QPushButton("Update Blog")
        dash_layout.addWidget(update_blog_button)
        update_blog_button.clicked.connect(self.open_update_blog)

        #Delete blog operations
        self.delete_mode = 0
        delete_blog_button = QPushButton("Delete Blog")
        dash_layout.addWidget(delete_blog_button)
        delete_blog_button.clicked.connect(self.open_delete_blog)


        #LOGOUT OPERATIONS
        logout_button = QPushButton("Logout")
        dash_layout.addWidget(logout_button)
        logout_button.clicked.connect(self.clicked_logout.emit)

        layout.addWidget(self.dash)

        #CONTENT
        self.content = QWidget()
        self.content_layout = QVBoxLayout()
        self.content.setLayout(self.content_layout)
        layout.addWidget(self.content, stretch=1)



    def open_search_blog(self):
        self.clear_content()

        search_label = QLabel("Search For Blog")
        key_label = QLabel("Search Key:")
        key_input = QLineEdit()
        search_button = QPushButton("Search")

        self.content_layout.addWidget(search_label)
        self.content_layout.addWidget(key_label)
        self.content_layout.addWidget(key_input)
        self.content_layout.addWidget(search_button)

        search_button.clicked.connect(lambda: self.do_search_blog(key_input.text()))

    def do_search_blog(self, key):
        self.clear_content()

        try:
            blog = self.controller.search_blog(key)

            if blog is not None:
                self.content_layout.addWidget(QLabel(f"ID: {blog.id}"))
                self.content_layout.addWidget(QLabel(f"Name: {blog.name}"))
                self.content_layout.addWidget(QLabel(f"URL: {blog.url}"))
                self.content_layout.addWidget(QLabel(f"Email: {blog.email}"))

            if self.delete_mode == 1:
                delete_button = QPushButton("DELETE")
                self.content_layout.addWidget(delete_button)
                self.delete_mode = 0
                delete_button.clicked.connect(lambda: self.do_delete_blog(blog.id))

            elif blog is None:
                self.content_layout.addWidget(QLabel(f"No blog found"))

        except Exception as e:
            self.content_layout.addWidget(QLabel(str(e)))

    def open_retrieve_blog(self):
        self.clear_content()

        search_label = QLabel("Retrieve Blog")
        search_string = QLabel("Search string:")
        string_input = QLineEdit()
        retrieve_button = QPushButton("Retrieve")

        self.content_layout.addWidget(search_label)
        self.content_layout.addWidget(search_string)
        self.content_layout.addWidget(string_input)
        self.content_layout.addWidget(retrieve_button)

        self.table_view = QTableView()

        retrieve_button.clicked.connect(lambda: self.do_retrieve_blog(string_input.text()))

    def do_retrieve_blog(self, string):
        self.clear_content()
        self.content_layout.addWidget(self.table_view)

        try:
            blogs = self.controller.retrieve_blogs(string)

            table = QStandardItemModel()
            table.setHorizontalHeaderLabels(["ID", "NAME", "URL", "EMAIL"])

            for b in blogs:
                row_items = [QStandardItem(str(b.id)), QStandardItem(str(b.name)), QStandardItem(str(b.url)), QStandardItem(str(b.email))]

                table.appendRow(row_items)

            self.table_view.setModel(table)

        except Exception as e:
            self.content_layout.addWidget(QLabel(str(e)))


    def open_create_blog(self):
        self.clear_content()

        create_label = QLabel("Create Blog")

        id_label = QLabel("Blog ID:")
        self.id_input = QLineEdit()

        name_label = QLabel("Blog Name:")
        self.name_input = QLineEdit()

        url_label = QLabel("Blog URL:")
        self.url_input = QLineEdit()

        email_label = QLabel("Blog Email:")
        self.email_input = QLineEdit()

        create_button = QPushButton("Create")

        self.content_layout.addWidget(create_label)
        self.content_layout.addWidget(id_label)
        self.content_layout.addWidget(self.id_input)
        self.content_layout.addWidget(name_label)
        self.content_layout.addWidget(self.name_input)
        self.content_layout.addWidget(url_label)
        self.content_layout.addWidget(self.url_input)
        self.content_layout.addWidget(email_label)
        self.content_layout.addWidget(self.email_input)
        self.content_layout.addWidget(create_button)

        create_button.clicked.connect(lambda: self.do_create_blog())

    def do_create_blog(self):
        self.clear_content()

        try:
            blog = self.controller.create_blog(self.id_input.text(), self.name_input.text(), self.url_input.text(), self.email_input.text())

            self.content_layout.addWidget(QLabel(f"Blog Created"))
            self.content_layout.addWidget(QLabel(f"ID: {blog.id}"))
            self.content_layout.addWidget(QLabel(f"Name: {blog.name}"))
            self.content_layout.addWidget(QLabel(f"URL: {blog.url}"))
            self.content_layout.addWidget(QLabel(f"Email: {blog.email}"))

        except Exception as e:
            self.content_layout.addWidget(QLabel(str(e)))

    def open_update_blog(self):
        self.clear_content()

        update_label = QLabel("Update Blog")
        id_label = QLabel("Blog ID:")
        id_input = QLineEdit()
        search_button = QPushButton("Search")

        self.content_layout.addWidget(update_label)
        self.content_layout.addWidget(id_label)
        self.content_layout.addWidget(id_input)
        self.content_layout.addWidget(search_button)

        search_button.clicked.connect(lambda: self.open_edit_update_blog(id_input.text()))


    def open_edit_update_blog(self, id):
        self.clear_content()
        blog = self.controller.search_blog(id)

        update_label = QLabel("Update Blog")

        id_label = QLabel("Blog ID:")
        id_input = QLineEdit()
        id_input.setText(str(blog.id))

        name_label = QLabel("Blog Name:")
        name_input = QLineEdit()
        name_input.setText(str(blog.name))

        url_label = QLabel("Blog URL:")
        url_input = QLineEdit()
        url_input.setText(str(blog.url))

        email_label = QLabel("Blog Email:")
        email_input = QLineEdit()
        email_input.setText(str(blog.email))

        update_button = QPushButton("UPDATE")

        self.content_layout.addWidget(update_label)
        self.content_layout.addWidget(id_label)
        self.content_layout.addWidget(id_input)

        self.content_layout.addWidget(name_label)
        self.content_layout.addWidget(name_input)

        self.content_layout.addWidget(url_label)
        self.content_layout.addWidget(url_input)

        self.content_layout.addWidget(email_label)
        self.content_layout.addWidget(email_input)

        self.content_layout.addWidget(update_button)

        update_button.clicked.connect(lambda: self.do_update_blog(blog.id, id_input.text(), name_input.text(), url_input.text(), email_input.text()))

    def do_update_blog(self, key, new_id, new_name, new_url, new_email):
        self.clear_content()

        try:
            updated = self.controller.update_blog(key, new_id, new_name, new_url, new_email)

            if updated:
                self.content_layout.addWidget(QLabel("Updated Blog:"))
                self.content_layout.addWidget(QLabel(f"ID: {new_id}"))
                self.content_layout.addWidget(QLabel(f"Name: {new_name}"))
                self.content_layout.addWidget(QLabel(f"URL: {new_url}"))
                self.content_layout.addWidget(QLabel(f"Email: {new_email}"))
            else:
                self.content_layout.addWidget(QLabel("Update Failed"))

        except Exception as e:
            self.content_layout.addWidget(QLabel(str(e)))

    def open_delete_blog(self):
        self.clear_content()
        self.delete_mode = 1

        delete_label = QLabel("Delete Blog")
        id_label = QLabel("Blog ID:")
        id_input = QLineEdit()
        search_button = QPushButton("Search")

        self.content_layout.addWidget(delete_label)
        self.content_layout.addWidget(id_label)
        self.content_layout.addWidget(id_input)
        self.content_layout.addWidget(search_button)

        search_button.clicked.connect(lambda: self.do_search_blog(id_input.text()))



    def do_delete_blog(self, key):
        self.clear_content()
        warning_label = QLabel("Are you sure you want to delete?")
        self.content_layout.addWidget(warning_label)
        DELETE_button = QPushButton("DELETE")
        self.content_layout.addWidget(DELETE_button)

        DELETE_button.clicked.connect(lambda: self.confirm_delete(key))

    def confirm_delete(self, key):
        self.clear_content()

        try:
            result_list = self.controller.delete_blog(key)

            if result_list:
                self.content_layout.addWidget(QLabel("Blog Deleted"))
            else:
                self.content_layout.addWidget(QLabel("Blog Not Found"))

        except Exception as e:
            self.content_layout.addWidget(QLabel(str(e)))



    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
