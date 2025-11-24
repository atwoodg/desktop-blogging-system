import json

from blogging.blog import Blog

class BlogDecoder(json.JSONDecoder):
    """Helper to decode Blog objects from JSON."""

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if {"id", "name", "url", "email"}.issubset(obj.keys()):
            return Blog(obj["id"], obj["name"], obj["url"], obj["email"])
        return obj