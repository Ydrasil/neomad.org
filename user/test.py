from unittest import TestCase

from user.views import *
from trips.views import *
from blog.views import *
from auth.views import *


class UserTest(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user = User(email='test@email.com').set_password('test').save()

    def tearDown(self):
        User.objects.delete()

    def test_profile(self):
        result = self.client.get('/@none')
        self.assertEqual(result.status_code, 200)

    def test_wrong_profile(self):
        result = self.client.get('/@doesnotexist')
        self.assertEqual(result.status_code, 404)
