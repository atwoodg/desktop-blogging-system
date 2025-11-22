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
        * each post is stored in its own .dat file under records_path
        * collections are loaded from disk when needed
    """

    def __init__(self, autosave=True):
        cfg = Configuration()
        self.autosave = autosave
        self.path = cfg.__class__.records_path
        self.ext = cfg.__class__.records_extension

        # in-memory list of posts for non-persistent mode
        self._posts = []

        if self.autosave:
            os.makedirs(self.path, exist_ok=True)

    # ---------- internal helpers ----------

    def _file_name(self, code):
        return os.path.join(self.path, f"{code}{self.ext}")

    def _load_single(self, code):
        """Load a single post from disk by code (persistent mode only)."""
        file_name = self._file_name(code)
        if not os.path.exists(file_name):
            return None
        try:
            with open(file_name, "rb") as f:
                return pickle.load(f)
        except Exception:
            return None

    def _load_all_from_disk(self):
        """Return all posts stored on disk, sorted by code ascending."""
        posts = []
        if not os.path.exists(self.path):
            return posts

        for fname in os.listdir(self.path):
            if not fname.endswith(self.ext):
                continue
            try:
                code = int(fname.replace(self.ext, ""))
            except ValueError:
                continue
            p = self._load_single(code)
            if isinstance(p, Post):
                posts.append(p)

        posts.sort(key=lambda p: p.code)
        return posts

    # ---------- DAO operations ----------

    def search_post(self, key):
        """Return post with given code, or None if it does not exist."""
        if not self.autosave:
            for p in self._posts:
                if p.code == key:
                    return p
            return None

        return self._load_single(key)

    def create_post(self, post):
        """Create a new post. Returns True on success."""
        if not isinstance(post, Post):
            return False

        if not self.autosave:
            self._posts.append(post)
            return True

        file_name = self._file_name(post.code)
        try:
            with open(file_name, "wb") as f:
                pickle.dump(post, f)
            return True
        except Exception:
            return False

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
        if not self.autosave:
            for p in self._posts:
                if p.code == key:
                    p.update_post(new_title, new_text)
                    return True
            return False

        p = self._load_single(key)
        if p is None:
            return False

        p.update_post(new_title, new_text)

        try:
            with open(self._file_name(key), "wb") as f:
                pickle.dump(p, f)
            return True
        except Exception:
            return False

    def delete_post(self, key):
        """Delete post with given code. Returns True if deleted."""
        if not self.autosave:
            for i, p in enumerate(self._posts):
                if p.code == key:
                    del self._posts[i]
                    return True
            return False

        file_name = self._file_name(key)
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                return True
            except Exception:
                return False
        return False

    def list_posts(self):
        """
        Return all posts for the current blog.
        For determinism we return them sorted by code ASC;
        the controller will sort DESC where needed.
        """
        if not self.autosave:
            posts = list(self._posts)
        else:
            posts = self._load_all_from_disk()

        posts.sort(key=lambda p: p.code)
        return posts
