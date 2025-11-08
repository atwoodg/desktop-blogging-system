from datetime import datetime


class Post:
    """Represents a single blog post."""

    def __init__(self, code, title, text, creation=None, update=None):
        """
        Initialize a Post.
        - code: integer post ID
        - title: post title
        - text: post content
        - creation: optional creation datetime (defaults to now)
        - update: optional update datetime (defaults to now)
        """
        self.code = code
        self.title = title
        self.text = text
        now = datetime.now()
        self.creation = creation if creation else now
        self.update = update if update else now

    def update_post(self, updated_title=None, updated_text=None, updated_time=None):
        """
        Update post title and/or text.
        Automatically updates the 'update' timestamp.
        Returns True if something was changed, otherwise False.
        """
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

    def __eq__(self, other):
        """Compare two Post objects for equality."""
        if isinstance(other, Post):
            return (
                self.code == other.code and
                self.title == other.title and
                self.text == other.text and
                int(self.creation.strftime("%Y%m%d%H%M%S")) == int(other.creation.strftime("%Y%m%d%H%M%S")) and
                int(self.update.strftime("%Y%m%d%H%M%S")) == int(other.update.strftime("%Y%m%d%H%M%S"))
            )
        return False

    def __str__(self):
        """Return a readable string version of the post."""
        return (
            f"Code: {self.code}\n"
            f"Date Posted: {self.creation}\n\n"
            f"{self.title}\n{self.text}\n\n"
            f"Last Updated: {self.update}"
        )

    def __repr__(self):
        """Return a developer-friendly representation of the post."""
        return (
            f"Post(code={self.code}, "
            f"title={self.title!r}, "
            f"text={self.text!r}, "
            f"creation={self.creation}, "
            f"update={self.update})"
        )
