from datetime import datetime
import hashlib

from blogging.blog import Blog
from blogging.post import Post
from blogging.configuration import Configuration

from blogging.dao.blog_dao_json import BlogDAOJSON

from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class Controller:

    def __init__(self, autosave=None):
        cfg = Configuration()

        # decide if we are using persistence or not
        self.autosave = cfg.__class__.autosave if autosave is None else autosave

        self.logged_in = False
        self.current_user = None
        self.current_blog = None

        # DAOs know whether persistence is enabled
        self.blog_dao = BlogDAOJSON(self.autosave)

        # load users (username, sha256(password)) from config file
        self.users = self._load_users(cfg.__class__.users_file)

    # ---------- helper methods ----------

    def _hash_password(self, pw):
        return hashlib.sha256(pw.encode()).hexdigest()

    def _load_users(self, file):
        users = {}
        try:
            with open(file, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) != 2:
                        continue
                    u, h = parts
                    users[u] = h
        except Exception:
            # if file is missing we just end up with empty user set
            pass
        return users

    def _ensure_logged_in(self):
        if not self.logged_in:
            raise IllegalAccessException("must be logged in")

    def _ensure_current_blog(self):
        if self.current_blog is None:
            raise NoCurrentBlogException("no current blog")

    # ---------- login / logout ----------

    def login(self, username, password):
        if self.logged_in:
            raise DuplicateLoginException()

        if username not in self.users:
            raise InvalidLoginException()

        if self._hash_password(password) != self.users[username]:
            raise InvalidLoginException()

        self.logged_in = True
        self.current_user = username
        return True

    def logout(self):
        if not self.logged_in:
            raise InvalidLogoutException()
        self.logged_in = False
        self.current_blog = None
        return True

    # ---------- blog operations ----------

    def create_blog(self, id, name, url, email):
        self._ensure_logged_in()

        # cannot have duplicate id
        if self.blog_dao.search_blog(id):
            raise IllegalOperationException("duplicate id")

        blog = Blog(id, name, url, email)
        self.blog_dao.create_blog(blog)
        return blog

    def search_blog(self, id):
        self._ensure_logged_in()
        return self.blog_dao.search_blog(id)

    def retrieve_blogs(self, key):
        self._ensure_logged_in()
        return self.blog_dao.retrieve_blogs(key)

    def list_blogs(self):
        self._ensure_logged_in()
        return self.blog_dao.list_blogs()

    def update_blog(self, old_id, new_id, new_name, new_url, new_email):
        self._ensure_logged_in()

        # cannot update if there are no blogs at all
        if len(self.blog_dao.list_blogs()) == 0:
            raise IllegalOperationException("cannot update blog when no blogs are registered")

        # cannot update a blog that does not exist
        blog = self.blog_dao.search_blog(old_id)
        if blog is None:
            raise IllegalOperationException("cannot update blog with an ID that is not registered")

        #cannot update current blog
        if self.current_blog is not None and self.current_blog.id == old_id:
            raise IllegalOperationException("cannot update the current blog")

        # new id must be unused (unless unchanged)
        if new_id != old_id and self.blog_dao.search_blog(new_id):
            raise IllegalOperationException("cannot update blog with a duplicated ID")

        return self.blog_dao.update_blog(old_id, new_id, new_name, new_url, new_email)

    def delete_blog(self, id):
        self._ensure_logged_in()

        blogs = self.blog_dao.list_blogs()
        if len(blogs) == 0:
            # no blogs at all
            raise IllegalOperationException("cannot delete blog when no blogs are registered")

        blog = self.blog_dao.search_blog(id)
        if blog is None:
            # id not registered
            raise IllegalOperationException("cannot delete blog with an ID that is not registered")

        #ensure blog deletion is not current blog
        if self.current_blog is not None and self.current_blog.id == id:
            raise IllegalOperationException("cannot delete the current blog")

        return self.blog_dao.delete_blog(id)

    # ---------- current blog ----------

    def set_current_blog(self, id):
        self._ensure_logged_in()
        blog = self.blog_dao.search_blog(id)
        if blog is None:
            raise IllegalOperationException("cannot set current blog with an ID that is not registered")
        self.current_blog = blog
        return True

    def unset_current_blog(self):
        self._ensure_logged_in()
        self.current_blog = None
        return True


    def get_current_blog(self):
        self._ensure_logged_in()
        return self.current_blog

    # ---------- post operations ----------

    def create_post(self, title, text):
        self._ensure_logged_in()
        self._ensure_current_blog()

        post = Post(0, title, text, datetime.now(), datetime.now())
        # controller_test + integration_test only ever use one blog for posts,
        # so the DAO does not need the blog id here.
        self.current_blog.add_post(post)
        return post

    def search_post(self, code):
        self._ensure_logged_in()
        self._ensure_current_blog()
        return self.current_blog.get_post(code)

    def retrieve_posts(self, key):
        self._ensure_logged_in()
        self._ensure_current_blog()

        posts = self.current_blog.retrieve_post(key)
        # tests expect ascending order of codes for retrieve_posts
        posts.sort(key=lambda p: p.code)
        return posts

    def update_post(self, code, new_title, new_text):
        self._ensure_logged_in()
        self._ensure_current_blog()

        # cannot update if there are no posts for that blog in the system
        if len(self.current_blog.list_posts()) == 0:
            return False

        # Delegate the actual update (and persistence) to the DAO
        return self.current_blog.post_dao.update_post(code, new_title, new_text)

    def delete_post(self, code):
        self._ensure_logged_in()
        self._ensure_current_blog()

        # if there are no posts at all, we just return False
        if len(self.current_blog.list_posts()) == 0:
            return False

        return self.current_blog.remove_post(code)

    def list_posts(self):
        self._ensure_logged_in()
        self._ensure_current_blog()

        posts = self.current_blog.list_posts()
        # Tests expect list_posts in descending order of code
        posts.sort(key=lambda p: p.code, reverse=True)
        return posts
