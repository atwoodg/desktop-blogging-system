from blogging.blog import Blog
from blogging.post import Post
from datetime import datetime

class Controller:
    """
    Controller: holds login state and manages blogs/posts.
    Step 1: just login/logout and basic attributes.
    """

    def __init__(self):
        self.logged_in = False
        self.blogs = []           # list[Blog]
        self.current_blog = None  # Blog or None
        self.next_post_code = 1   # global post id counter across all blogs

    # ---------- LOGIN / LOGOUT ----------
    def login(self, username, password):
        # only one valid pair per spec/tests
        if self.logged_in:
            return False
        if username == "user" and password == "blogging2025":
            self.logged_in = True
            return True
        return False

    def logout(self):
        if not self.logged_in:
            return False
        self.logged_in = False
        self.current_blog = None
        return True
