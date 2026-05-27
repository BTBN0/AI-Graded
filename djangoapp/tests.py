from django.test import TestCase, Client
from django.contrib.auth.models import User
import json


class DealerAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123',
            first_name='Test', last_name='User', email='test@test.com'
        )

    def test_get_all_dealers(self):
        response = self.client.get('/djangoapp/get_dealers/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 200)
        self.assertIn('dealers', data)

    def test_get_dealer_by_id(self):
        response = self.client.get('/djangoapp/dealer/1/')
        self.assertEqual(response.status_code, 200)

    def test_get_dealers_by_state(self):
        response = self.client.get('/djangoapp/get_dealers/Kansas/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        for dealer in data['dealers']:
            self.assertEqual(dealer['state'], 'Kansas')

    def test_get_dealer_reviews(self):
        response = self.client.get('/djangoapp/reviews/dealer/1/')
        self.assertEqual(response.status_code, 200)

    def test_analyze_review_positive(self):
        response = self.client.get('/djangoapp/analyze_review/?text=Fantastic+services')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['sentiment'], 'positive')

    def test_login(self):
        response = self.client.post(
            '/djangoapp/login/',
            json.dumps({'userName': 'testuser', 'password': 'testpass123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'Authenticated')

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/djangoapp/logout/')
        self.assertEqual(response.status_code, 200)
