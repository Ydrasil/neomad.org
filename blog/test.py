import os
from unittest import TestCase

from core import app
from .models import Article
from user.models import User


def login_user(self):
    data = {
        'email': 'emailtest@test.com',
        'password': 'testtest',
    }
    self.client.post('/login', data=data, follow_redirects=True)


class ArticleTest(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user = User(email='emailtest@test.com',
                         username='emailtest').set_password('testtest')
        self.user.allow_localization = True
        self.user.save()

    def tearDown(self):
        User.objects.delete()

    def test_like_an_article(self):
        user = User(email='author@test.com',
                    username='author').set_password('testtest').save()
        article = Article(title='title', content='<p>content</p>')
        article.author = user
        article.save()
        id_article = Article.objects.first().id
        login_user(self)
        result = self.client.get('/article/' + str(id_article) + '/like')
        self.assertEqual(result.status_code, 302)
        user = User.objects.get(email='emailtest@test.com')
        self.assertEqual(user.article_liked.id, id_article)

    def test_title_clean_html(self):
        article = Article(title='<h1>title<br></h1>', content='').save()
        self.assertEqual(article.title, 'title')

    def test_content_cleaned_html(self):
        article = Article(title='', content='<p>content</p>').save()
        self.assertEqual(article.content, '<p>content</p>')
        article = Article(title='',
                          content='<p style="font: Arial">content</p>').save()
        self.assertEqual(article.content, '<p>content</p>')
        article = Article(title='',
                          content='<p><img src="/static/img"></p>').save()
        self.assertEqual(article.content, '<p><img src="/static/img"/></p>')
        article = Article(title='',
                          content='<p><em>emphased content</em><i>also emphased</i></p>').save()
        self.assertEqual(article.content, '<p><em>emphased content</em><em>also emphased</em></p>')

    def test_delete_article_and_folders_pictures(self):
        article = Article(title='<h1>title<br></h1>', content='<p>content</p>').save()
        self.assertTrue(os.path.isdir(article.get_images_path()))
        Article.objects.get(id=article.id).delete()
        self.assertFalse(os.path.isdir(article.get_images_path()))

    def test_language_detection(self):
        article = Article(title='Un titre en français',
                          content='<p>Voici le contenu de l\'article qui est '
                                  'lui aussi en français</p>').save()
        self.assertEqual(article.language, 'fr')

        article = Article(title='A title in English',
                          content='<p>The content of the article is in '
                                  'English</p>').save()
        self.assertTrue(article.language, 'en')
