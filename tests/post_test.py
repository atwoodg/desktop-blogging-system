import unittest
from blogging.post import Post
from datetime import datetime

class PostTest(unittest.TestCase):

    def setUp(self):
        self.post = Post(1, "Test Title", "Test Text", datetime(2025, 4, 30, 12, 30), datetime(2025, 4, 30, 12, 45))

    #Testing proper initialization
    def test_post_init(self):
        self.assertEqual(self.post.code, 1)
        self.assertEqual(self.post.title, "Test Title")
        self.assertEqual(self.post.text, "Test Text")
        self.assertEqual(self.post.creation, datetime(2025, 4, 30, 12, 30))
        self.assertEqual(self.post.update, datetime(2025, 4, 30, 12, 45))

    #Testing proper title, text and update time
    def test_post_update(self):
        old_time = self.post.update #Marking old update time
        new_time = datetime(2025, 5, 1, 4, 30)
        self.post.update_post("New Title", "New Text", new_time) #updating post

        #Testing equality of all variables
        self.assertEqual(self.post.title, "New Title")
        self.assertEqual(self.post.text, "New Text")
        self.assertEqual(self.post.update, new_time)
        self.assertNotEqual(self.post.update, old_time)

    #Tests that eq method correctly determines equality
    def test_post_eq(self):
        example_post = Post(1, "Test Title", "Test Text", datetime(2025, 4, 30, 12, 30), datetime(2025, 4, 30, 12, 45))
        self.assertEqual(self.post, example_post)

    #Tests output contain proper text and title
    def test_post_str(self):
        example_output = str(self.post)
        self.assertIn("Test Title", example_output)
        self.assertIn("Test Text", example_output)
        self.assertIn(str(self.post.code), example_output)






