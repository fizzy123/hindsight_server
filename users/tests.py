from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from users.models import HindsightUser

class UserViewTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('test', 'test@test.com', 'testing_pw')
        h_user1 = HindsightUser(user=user1)
        h_user1.save()
        user1.save()
        
        user2 = User.objects.create_user('tester', 'tester@test.com', 'pw_test')
        h_user2 = HindsightUser(user=user2)
        h_user2.save()
        user2.save()

    def test_successful_login_view(self):
        response = self.client.post(reverse('users:login'), {'username':'test','password':'testing_pw'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)

    def test_unsuccessful_login_view(self):
        response = self.client.post(reverse('users:login'), {'username':'tsxest','password':'teasting_pw'})
        self.assertEqual(response.status_code, 403) 

    def test_create_user_view(self):
        response = self.client.post(reverse('users:create'), {'username':'blah','email':'blah@test.com','password':'blah_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(User.objects.get(username='blah'))


    def test_successful_logout_view(self):
        self.client.login(username='test', password='testing_pw')
        response = self.client.post(reverse('users:logout'))
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(response.status_code, 200)
        
    def test_verified_login_view(self):
        response = self.client.post(reverse('users:create'), {'username':'unverify','email':'unverify@test.com','password':'unverify'})
        response = self.client.post(reverse('users:login'), {'username':'unverify', 'password': 'unverify'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)
#        self.assertFalse(User.objects.get(email='blah@test.com').is_active)
"""
    def test_successful_verify_view(self):
        self.client.login(username='test', password='testing_pw')
        response  = self.client.post(reverse('users:verify'))
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_verify_view(self):
        response  = self.client.post(reverse('users:verify'))
        self.assertEqual(response.status_code, 403)
"""
"""
    def test_verify_email_view(self):
        response = self.client.post(reverse('users:create'), {'username':'verify','email':'verify@test.com','password':'verify'})
        user = User.objects.get(email = 'verify@test.com')
        response = self.client.get(reverse('users:verify_email', args=(HindsightUser.objects.get(user = user).key,)))
        user = User.objects.get(email = 'verify@test.com')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_active)

    def test_unverified_login_view(self):
        response = self.client.post(reverse('users:create'), {'username':'unverify','email':'unverify@test.com','password':'unverify'})
        response = self.client.post(reverse('users:login'), {'username':'unverify', 'password': 'unverify'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, "NOT_ACTIVE")
"""


