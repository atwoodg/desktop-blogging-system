from datetime import datetime
import hashlib

from blogging.blog import Blog
from blogging.post import Post
from blogging.configuration import Configuration

from blogging.dao.blog_dao_json import BlogDAOJSON
from blogging.dao.post_dao_pickle import PostDAOPickle

from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class Controller:

    def __init__(self, autosave=None):
        cfg = Configuration()
        if autosave is None:
            self.autosave = cfg.__class__.autosave
        else:
            self.autosave = autosave

        self.logged_in = False
        self.current_user = None
        self.current_blog = None

        # DAO managers
        self.blog_dao = BlogDAOJSON()
        self.post_dao = PostDAOPickle()

        # set next post code based on files already stored
        existing = self.post_dao.list_posts()
        if existing:
            self.next_post_code = max(p.code for p in existing) + 1
        else:
            self.next_post_code = 1

        self.users = self._load_users(cfg.__class__.users_file)

    # ---------- helpers ----------
    def _hash_password(self, plain_password: str) -> str:
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

    def _load_users(self, users_file):
        users = {}
        try:
            with open(users_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 2:
                        continue
                    username = parts[0].strip()
                    digest = parts[1].strip()
                    users[username] = digest
        except FileNotFoundError:
            pass
        return users

    def _ensure_logged_in(self):
        if not self.logged_in:
            raise IllegalAccessException("must be logged in")

    def _ensure_current_blog(self):
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog selected")

    # ---------- login/logout ----------
    def login(self, username, password):
        if self.logged_in:
            raise DuplicateLoginException("already logged in")
        if username not in self.users:
            raise InvalidLoginException("bad user")
        if self._hash_password(password) != self.users[username]:
            raise InvalidLoginException("bad password")

        self.logged_in = True
        self.current_user = username
        return True

    def logout(self):
        if not self.logged_in:
            raise InvalidLogoutException("not logged in")
        self.logged_in = False
        self.current_user = None
        self.current_blog = None
        return True

    # ---------- blog ops ----------
    def create_blog(self, id, name, url, email):
        self._ensure_logged_in()

        if self.blog_dao.search_blog(id) is not None:
            raise IllegalOperationException("duplicate id")

        b = Blog(id, name, url, email)
        self.blog_dao.create_blog(b)
        return b

    def search_blog(self, id):
        self._ensure_logged_in()
        return self.blog_dao.search_blog(id)

    def retrieve_blogs(self, keyword):
        self._ensure_logged_in()
        return self.blog_dao.retrieve_blogs(keyword)

    def list_blogs(self):
        self._ensure_logged_in()
        return self.blog_dao.list_blogs()

    def update_blog(self, old_id, new_id, new_name, new_url, new_email):
        self._ensure_logged_in()
        if self.current_blog and self.current_blog.id == old_id:
            raise IllegalOperationException("cannot update active blog")

        if self.blog_dao.search_blog(old_id) is None:
            raise IllegalOperationException("no blog to update")

        if new_id != old_id and self.blog_dao.search_blog(new_id):
            raise IllegalOperationException("id already exists")

        newBlog = Blog(new_id, new_name, new_url, new_email)
        return self.blog_dao.update_blog(old_id, newBlog)

    def delete_blog(self, id):
        self._ensure_logged_in()
        if self.current_blog and self.current_blog.id == id:
            raise IllegalOperationException("cannot delete active blog")

        if not self.blog_dao.delete_blog(id):
            raise IllegalOperationException("cannot delete blog")
        return True

    # ---------- current blog ----------
    def set_current_blog(self, id):
        self._ensure_logged_in()
        result = self.blog_dao.search_blog(id)
        if result is None:
            raise IllegalOperationException("blog missing")
        self.current_blog = result

    def unset_current_blog(self):
        self.current_blog = None

    def get_current_blog(self):
        self._ensure_logged_in()
        return self.current_blog

    # ---------- posts ----------
    def create_post(self, title, text):
        self._ensure_logged_in()
        self._ensure_current_blog()

        p = Post(self.next_post_code, title, text, datetime.now(), datetime.now())
        self.post_dao.create_post(p)
        self.next_post_code += 1
        return p

    def search_post(self, code):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.search_post(code)

    def retrieve_posts(self, keyword):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.retrieve_posts(keyword)

    def list_posts(self):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.list_posts()

    def update_post(self, code, title, text):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.update_post(code, title, text)

    def delete_post(self, code):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.post_dao.delete_post(code)
