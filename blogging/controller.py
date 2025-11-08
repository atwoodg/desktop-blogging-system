from blogging.blog import Blog
from blogging.post import Post
from datetime import datetime

class Controller:
    """
    Step 2: add blog read ops: create_blog, search_blog, retrieve_blogs, list_blogs.
    """

    def __init__(self):
        self.logged_in = False
        self.blogs = []
        self.current_blog = None
        self.next_post_code = 1

    # ---------- LOGIN / LOGOUT ----------
    def login(self, username, password):
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

    # ---------- BLOG READ OPS ----------
    def create_blog(self, id, name, url, email):
        if not self.logged_in:
            return None
        # no duplicate ids
        for b in self.blogs:
            if b.id == id:
                return None
        blog = Blog(id, name, url, email)
        self.blogs.append(blog)
        return blog

    def search_blog(self, id):
        if not self.logged_in:
            return None
        for b in self.blogs:
            if b.id == id:
                return b
        return None

    def retrieve_blogs(self, keyword):
        if not self.logged_in:
            return None
        out = []
        kw = (keyword or "").lower()
        for b in self.blogs:
            if kw in b.name.lower():
                out.append(b)
        return out

    def list_blogs(self):
        if not self.logged_in:
            return None
        return list(self.blogs)
