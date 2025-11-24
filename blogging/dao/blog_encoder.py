import json

from blogging.blog import Blog

class BlogEncoder(json.JSONEncoder):
    """Helper to encode Blog objects as JSON."""

    def default(self, obj):
        if isinstance(obj, Blog):
            return {
                "id": obj.id,
                "name": obj.name,
                "url": obj.url,
                "email": obj.email,
            }
        return super().default(obj)