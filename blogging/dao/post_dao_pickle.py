import os
import pickle

from blogging.configuration import Configuration
from blogging.dao.post_dao import PostDAO
from blogging.post import Post


class PostDAOPickle(PostDAO):
    """
    Post DAO with optional persistence.

    - If autosave == False:
        * posts live only in memory (used by controller unit tests)
    - If autosave == True:
        * each blog is stored in its own .dat file under records_path
        * .dat file contains list of post objects
        * collections are loaded from disk when needed
    """

    def __init__(self, blog, autosave=True):
        cfg = Configuration()
        self.autosave = autosave
        self.path = cfg.__class__.records_path
        self.ext = cfg.__class__.records_extension
        self.blog = blog

        # in-memory list of posts for non-persistent mode
        self._posts = []

        # code counter
        self._next_code = 1

        os.makedirs(self.path, exist_ok=True)

        self._file = self._file_name(self.blog.id)

        if self.autosave:
            if os.path.exists(self._file):
                self._load()
            else:
                self._write([])

    # ---------- internal helpers ----------

    def _file_name(self, code):
        return os.path.join(self.path, f"{code}{self.ext}")

    def _load(self):

        try:
            with open(self._file, "rb") as f:
                content = pickle.load(f)
            if isinstance(content, list):
                self._posts = [p for p in content if isinstance(p, Post)]
            else: self._posts = []

        except Exception:
            return None

        if len(self._posts) == 0:
            self._next_code = 1
        else:
            max_code = max((p.code for p in self._posts), default = 0)
            self._next_code = max_code + 1

    def _load_all_from_disk(self):
        """Return all posts stored on disk"""
        return list(self._posts)

    def _write(self, posts):

        if not self.autosave:
            return True

        try:
            with open(self._file, "wb") as f:
                pickle.dump(self._posts, f)
            return True
        except Exception:
            return False


    # ---------- DAO operations ----------

    def search_post(self, key):
        """Return post with given code, or None if it does not exist."""
        if not self.autosave:
            for p in self._posts:
                if p.code == key:
                    return p
            return None

        for p in self._posts:
            if p.code == key:
                return p
        return None

    def create_post(self, post):
        """Create a new post. Returns True on success."""
        if not isinstance(post, Post):
            return None

        if not getattr(post, "code", None):
            post.code = self._next_code
            self._next_code += 1
        else:
            if post.code >= self._next_code:
                self._next_code = post.code + 1

        self._posts.append(post)

        if self.autosave:
            write = self._write(self._posts)
            if not write:
                self._posts.pop()
                return None
        return post

    def retrieve_posts(self, search_string):
        """
        Return posts whose title or text contain search_string (case-insensitive),
        ordered by code ASCENDING.

        Integration + controller tests expect retrieve_posts("journey") to
        give [1, 3, 5] in that order.
        """
        if search_string is None:
            search_string = ""
        key = search_string.lower()

        if not self.autosave:
            base = list(self._posts)
        else:
            base = self._load_all_from_disk()

        base.sort(key=lambda p: p.code)

        result = []
        for p in base:
            if key in p.title.lower() or key in p.text.lower():
                result.append(p)
        return result

    def update_post(self, key, new_title, new_text):
        """Update title/text of a post. Returns True if updated."""
        # find post
        for p in self._posts:

            if p.code == key:
                p.update_post(new_title, new_text)

                # persist list
                if self.autosave:
                    return self._write(self._posts)
                return True

        return False

    def delete_post(self, key):
        """Delete post with given code. Returns True if deleted."""
        deleted = False
        new_list = []
        for p in self._posts:
            if not deleted and p.code == key:
                deleted = True
                continue
            new_list.append(p)

        if deleted:
            self._posts = new_list
            if self.autosave:
                self._write(self._posts)
        return deleted

    def list_posts(self):
        """
        Return all posts for the current blog.
        For determinism we return them sorted by code ASC;
        the controller will sort DESC where needed.
        """
        return sorted(self._posts, key = lambda p: p.code)
