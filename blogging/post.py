# post.py
# SENG 265 Assignment 3
# Author: Gabriel Atwood, Michael Chen
# Post class for handling blog post creation, updates, and equality checking.

from datetime import datetime

class Post:
    # initializes blog post
    def __init__(self, code, title, text, creation=None, update=None):
        # identifying number, title, and content
        self.code = code
        self.title = title
        self.text = text
        now = datetime.now()
        self.creation = creation if creation else now
        self.update = update if update else now

    # update existing post title or text
    def update_post(self, updated_title=None, updated_text=None, updated_time=None):
        changed = False
        if updated_text is not None:
            self.text = updated_text
            changed = True
        if updated_title is not None:
            self.title = updated_title
            changed = True
        if changed:
            self.update = updated_time if updated_time else datetime.now()
            return True
        return False

    # equality comparison
    def __eq__(self, other):
        if isinstance(other, Post):
            return (self.code == other.code and
                    self.title == other.title and
                    self.text == other.text and
                    int(self.creation.strftime("%Y%m%d%H%M%S")) == int(other.creation.strftime("%Y%m%d%H%M%S")) and
                    int(self.update.strftime("%Y%m%d%H%M%S")) == int(other.update.strftime("%Y%m%d%H%M%S")))
        return False

    # readable string
    def __str__(self):
        return f"Code: {self.code}\nDate Posted: {self.creation}\n\n{self.title}\n{self.text}\n\nLast Updated: {self.update}"

    # developer-readable string
    def __repr__(self):
        return f"Post(code={self.code}, title={self.title}, text={self.text}, creation={self.creation}, update={self.update})"
