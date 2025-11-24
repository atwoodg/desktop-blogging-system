from blogging.dao.post_dao_pickle import PostDAOPickle
from blogging.configuration import Configuration

class Blog:

    def __init__(self, id, name, url, email):
        self.id = id
        self.name = name
        self.url = url
        self.email = email
        self.dao = PostDAOPickle(self)
        autosave = Configuration.autosave
        self.post_dao = PostDAOPickle(self, autosave)

    def add_post(self, post):
        return self.post_dao.create_post(post)

    def get_post(self, code):
        return self.post_dao.search_post(code)

    def list_posts(self):
        return self.post_dao.list_posts()

    def remove_post(self, code):
        return self.post_dao.delete_post(code)

    def retrieve_post(self, key):
        return self.post_dao.retrieve_posts(key)

    def __str__(self):
        return f"Blog ID: {self.id}\nName: {self.name}\nURL: {self.url}\nEmail: {self.email}"

    def __eq__(self, other):
        return isinstance(other, Blog) and \
               self.id == other.id and \
               self.name == other.name and \
               self.url == other.url and \
               self.email == other.email
