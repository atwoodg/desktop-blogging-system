import json
import os

from blogging.blog import Blog
from blogging.configuration import Configuration
from blogging.dao.blog_dao import BlogDAO
from blogging.dao.blog_encoder import BlogEncoder
from blogging.dao.blog_decoder import BlogDecoder

class BlogDAOJSON(BlogDAO):
    """
    Blog DAO with optional persistence.

    - If autosave == False:
        * everything is purely in memory
        * we ignore any existing blogs.json on disk
    - If autosave == True:
        * blogs are loaded from blogs.json in the constructor
        * every create/update/delete writes the whole list back to file
    """

    def __init__(self, autosave=True):
        cfg = Configuration()
        self.autosave = autosave
        self.file_path = cfg.__class__.blogs_file

        # in-memory list of Blog objects
        self._blogs = []

        if self.autosave:
            # make sure the directory exists
            dir_name = os.path.dirname(self.file_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)

            # if file exists, load it; otherwise create empty file
            if os.path.exists(self.file_path):
                self._blogs = self._read_all()
            else:
                self._write_all([])

        # when autosave is False we simply start with an empty list and
        # never touch the file system – controller tests rely on that.

    # ---------- internal helpers ----------

    def _read_all(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f, cls=BlogDecoder)
            # json.load may return a single Blog or a list; normalize to list
            if isinstance(data, list):
                return [b for b in data if isinstance(b, Blog)]
            elif isinstance(data, Blog):
                return [data]
            else:
                return []
        except (IOError, json.JSONDecodeError):
            # if something goes wrong, treat as empty collection
            return []

    def _write_all(self, blogs):
        if not self.autosave:
            # in non-persistent mode we never touch the disk
            return
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(blogs, f, cls=BlogEncoder, indent=2)

    # ---------- DAO operations ----------

    def search_blog(self, key):
        """Return a blog whose id, name or url matches key, or None."""
        for b in self._blogs:
            if b.id == key or b.name == key or b.url == key:
                return b
        return None

    def create_blog(self, blog):
        """Append a new blog and persist if autosave is enabled."""
        self._blogs.append(blog)
        self._write_all(self._blogs)
        return True

    def retrieve_blogs(self, search_string):
        """
        Return blogs whose id/name/url/email contains search_string
        (case-insensitive). Empty search_string returns all blogs.
        """
        if not search_string:
            return list(self._blogs)

        s = str(search_string).lower()
        result = []
        for b in self._blogs:
            if (
                s in str(b.id).lower()
                or s in b.name.lower()
                or s in b.url.lower()
                or s in b.email.lower()
            ):
                result.append(b)
        return result

    def update_blog(self, key, new_id, new_name, new_url, new_email):
        """
        Replace the blog whose id == key with a new Blog.
        Returns True if something was updated, False otherwise.
        """
        updated = False
        for i, b in enumerate(self._blogs):
            if b.id == key:
                self._blogs[i] = Blog(new_id, new_name, new_url, new_email)
                updated = True
                break

        if updated:
            self._write_all(self._blogs)
        return updated

    def delete_blog(self, key):
        """
        Delete the blog whose id == key.
        Returns True if something was deleted, False otherwise.
        """
        deleted = False
        new_list = []
        for b in self._blogs:
            if not deleted and b.id == key:
                deleted = True
                continue
            new_list.append(b)

        if deleted:
            self._blogs = new_list
            self._write_all(self._blogs)

        return deleted

    def list_blogs(self):
        """Return a shallow copy of the current blog list."""
        return list(self._blogs)
