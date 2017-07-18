import json
from unittest import TestCase

from search.views import *
from user.models import User
from core import app


class SearchTest(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        User.objects.delete()
        Article.objects.delete()

    def test_search_retrieve_several_user(self):
        User(email='doejohn@test.com',
             username='doejohn').set_password('search').save()
        User(email='johndoe@test.com',
             username='johndoe').set_password('search').save()
        response = self.client.get('/search?q=john')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'doejohn', response.data)
        self.assertIn(b'johndoe', response.data)

    def test_search_retrieve_several_article(self):
        Article(title='<h1>My fries are cold<br></h1>',
                content='Why my french fries are cold?').save()
        Article(title='<h1>I like fries<br></h1>',
                content='I like fries').save()
        response = self.client.get('/search?q=fries')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My fries are cold', response.data)
        self.assertIn(b'I like fries', response.data)

    def test_search_retrieve_article_and_user(self):
        Article(title='<h1>My fries are cold<br></h1>',
                content='Why my french fries are cold ?').save()
        User(email='fries@test.com',
             username='friesuser').set_password('search').save()
        response = self.client.get('/search?q=fries')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My fries are cold', response.data)
        self.assertIn(b'friesuser', response.data)

    def test_search_maximum_10_users_and_articles(self):
        # Check that /search retrieve 10 users and 10
        # articles among 11 users and articles created
        for i in range(0, 11):
            Article(title='<h1>My fries are cold<br></h1>',
                    content='Why my french fries are cold ?').save()
            User(email='fries{}@test.com'.format(i),
                 username='friesuser{}'.format(i)).set_password(
                'search').save()
        response = self.client.get('/search?q=fries')
        self.assertEqual(response.status_code, 200)
        count = 0
        for word in response.data.split():
            if b'fries' in word:
                count = count + 1
        # /search?q=fries appear in response.data
        self.assertEqual(count, 21)
