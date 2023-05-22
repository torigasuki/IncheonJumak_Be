from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User,Verify

class SendEmailTest(APITestCase):
    def setUp(self):
        self.url = reverse('send_email')
        
    def test_send_email(self):
        email ={
            'email':'test@test.com'
        }
        response = self.client.post(self.url,email,format='json')
        self.assertEqual(response.status_code,200)
        
    def test_send_email_blank(self):
        email ={
            'email':''
        }
        response = self.client.post(self.url,email,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_send_email_not_email(self):
        email ={
            'email':'test'
        }
        response = self.client.post(self.url,email,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_send_email_already_send_email(self):
        verify = Verify.objects.create(email='test@test.com',code='123456')
        email ={
            'email':'test@test.com'
        }
        response = self.client.post(self.url,email,format='json')
        re_verify = Verify.objects.get(email=email['email'])
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(verify,re_verify.code)
    
    def test_send_email_already_register_email(self):
        User.objects.create(email='test@test.com',password='1234', nickname='test')
        email ={
            'email':'test@test.com'
        }
        response = self.client.post(self.url,email,format='json')
        self.assertEqual(response.status_code,400)