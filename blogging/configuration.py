import os

class Configuration():
    ''' configuration class for relevant persistence information '''
    autosave=True
    base = os.path.dirname(os.path.abspath(__file__))
    users_file = os.path.join(base, "users.txt")
    blogs_file = "bloggingJSON/blogs.json"
    records_path = "blogging/records"
    records_extension = ".dat"
    

