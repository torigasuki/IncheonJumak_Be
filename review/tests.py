from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from review.models import Review
from user.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test.client import MULTIPART_CONTENT,encode_multipart,BOUNDARY
from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file

# Create your tests here.
class reviewTest(APITestCase):
    def setUp(self):
        self.url = reverse('review_view')
        self.user =User.objects.create_user(email='test@test.com',nickname='test', password='test1234@')
        response = self.client.post(reverse('login'), {'email':'test@test.com','password':'test1234@'}, format='json')
        self.token = response.data.get('access')
        Review.objects.create(title='test', content='test', image='test', user=self.user)
        
    def test_review(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_create_with_image(self):
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = 'test.png'
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        data = {
            'title': 'test',
            'content': 'test',
            'user': self.user.id
        }
        data['image'] = image_file
        response = self.client.post(self.url, 
                                    data=encode_multipart(data=data,boundary=BOUNDARY ), 
                                    HTTP_AUTHORIZATION='Bearer ' + self.token,
                                    content_type=MULTIPART_CONTENT,
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_review_create_without_image(self):
        data = {
            'title': 'test',
            'content': 'test',
            'user': self.user.id
        }
        response = self.client.post(self.url, data=data,HTTP_AUTHORIZATION='Bearer ' + self.token, )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_review_create_without_title(self):
        data = {
            'content': 'test',
            'user': self.user.id
        }
        response = self.client.post(self.url, data=data,HTTP_AUTHORIZATION='Bearer ' + self.token, )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_without_content(self):
        data = {
            'title': 'test',
            'user': self.user.id
        }
        response = self.client.post(self.url, data=data,HTTP_AUTHORIZATION='Bearer ' + self.token, )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_review_create_without_authorization(self):
        data = {
            'title': 'test',
            'content': 'test',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)