from django.test import TestCase
from .models import Blog


class BlogTestCase(TestCase):
    def setUp(self):
        Blog.objects.create(title='Test', description='Test description', category='cat 1', author='Test author', position = 'Test position')

    def test_blog(self):
        blog = Blog.objects.get(title='Test')
        self.assertEqual(blog.title, 'Test')
        self.assertEqual(blog.description, 'Test description')


