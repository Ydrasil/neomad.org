import json

from unittest import TestCase

from around.models import Spot
from user.models import User
from api.views import *
from around.views import *
from trips.views import *


class ApiTest(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        Spot.objects.delete()
        User.objects.delete()

    def test_spot_create(self):
        user = User(email='spot@test.com',
                    username='spot').set_password('test')
        user.save()
        data = {
            'email': 'spot@test.com',
            'password': 'test'
        }
        self.client.post('/login', data=data, follow_redirects=True)
        data = {
            'name': 'spot',
            'wifi': 3,
            'coordinates': [10, 10],
            'power': False,
            'type': 'Coffee',
            'comment': 'Comment'
        }
        result = self.client.post('/api/spot', data=json.dumps(data),
                                  content_type='application/json')
        spot = Spot.objects.first()
        self.assertEqual(spot.user, User.objects.first())
        self.assertEqual(spot.location, [10, 10])
        self.assertEqual(spot.category, 'Coffee')
        self.assertEqual(spot.power_available, False)
        self.assertEqual(spot.comments, ['Comment'])
        self.assertEqual(result.status_code, 201)

    def test_spots_is_empty_when_no_spot(self):
        result = self.client.get('/api/spots')
        json_result = result.data.decode('utf8')
        data = json.loads(json_result)
        self.assertEqual(data, [])
        self.assertEqual(result.status_code, 200)
