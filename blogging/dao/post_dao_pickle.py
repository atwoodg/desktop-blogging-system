import os
import pickle
from blogging.post import Post
from blogging.configuration import Configuration
from blogging.dao.post_dao import PostDAO


class PostDAOPickle(PostDAO):

    def __init__(self):
        cfg = Configuration()
        self.path = cfg.__class__.records_path
        self.ext = cfg.__class__.records_extension

        # ensure directory exists
        os.makedirs(self.path, exist_ok=True)

    def _file(self, code):
        return os.path.join(self.path, f"{code}{self.ext}")

    # ---------- DAO methods ----------

    def search_post(self, key):
        file_path = self._file(key)
        if not os.path.exists(file_path):
            return None
        with open(file_path, "rb") as f:
            return pickle.load(f)

    def create_post(self, post):
        file_path = self._file(post.code)
        with open(file_path, "wb") as f:
            pickle.dump(post, f)
        return True

    def retrieve_posts(self, search_string):
        posts = self.list_posts()
        kw = (search_string or "").lower()
        result = []
        for p in posts:
            if kw in p.title.lower() or kw in p.text.lower():
                result.append(p)
        return result

    def update_post(self, key, new_title, new_text):
        post = self.search_post(key)
        if post is None:
            return False
        post.update_post(updated_title=new_title, updated_text=new_text)
        # save updated post
        with open(self._file(key), "wb") as f:
            pickle.dump(post, f)
        return True

    def delete_post(self, key):
        file_path = self._file(key)
        if not os.path.exists(file_path):
            return False
        os.remove(file_path)
        return True

    def list_posts(self):
        posts = []
        for filename in os.listdir(self.path):
            if filename.endswith(self.ext):
                code_str = filename.replace(self.ext, "")
                try:
                    code = int(code_str)
                    p = self.search_post(code)
                    if p:
                        posts.append(p)
                except ValueError:
                    pass
        # newest first (higher code)
        posts.sort(key=lambda p: p.code, reverse=True)
        return posts
