from datetime import datetime

class Post:
    #initializes blog post
    def __init__(self, code, title, text, creation, update):
        self.code = code
        self.title = title
        self.text = text
        self.creation = creation
        self.update = update

    #Updates a blog posts text and title if they are provided
    def update_post(self, updated_title=None, updated_text=None, updated_time=None):
        updated = False
        if updated_text is not None:
            self.text = updated_text
            updated = True

        if updated_title is not None:
            self.title = updated_title
            updated = True

        #if post is updated, changes update time to current time
        if updated == True:
            self.update = updated_time
            return True
        else:
            return False

    #Method to check if two posts are equal
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.code == other.code and
                    self.title == other.title and
                    self.text == other.text and
                    #turning datetime objects into ints of same format to check for equality
                    int(self.creation.strftime("%Y%m%d%H%M%S")) == int(other.creation.strftime("%Y%m%d%H%M%S")) and
                    int(self.update.strftime("%Y%m%d%H%M%S")) == int(other.update.strftime("%Y%m%d%H%M%S")))
        else:
            return False

    def __str__(self):
        return f"Code: {self.code}\nDate Posted: {self.creation}\n\n{self.title}\n{self.text}\n\nLast Updated: {self.update}"

    def __rep__(self):
        return f"code={self.code}, title={self.title}, text={self.text}, creation={self.creation}, update={self.update}"
