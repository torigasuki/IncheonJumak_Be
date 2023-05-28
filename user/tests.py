from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User,Verify, BookMark, Follow
from alchol.models import Alchol


class sendEmailTest(APITestCase):
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
        
class emailVerifyTest(APITestCase):
    def setUp(self):
        self.url = reverse('verify_email')
        self.verify = Verify.objects.create(email='test@test.com',code='123456')
        
    def test_email_verify(self):
        verify ={
            'email':'test@test.com',
            'code':'123456'
        }
        response = self.client.post(self.url,verify,format='json')
        self.assertEqual(response.status_code,200)
        
    def test_email_verify_not_match_code(self):
        verify ={
            'email':'test@test.com',
            'code':'654321'
        }
        response = self.client.post(self.url,verify,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_email_verify_not_match_email(self):
        verify ={
            'email':'test2@test.com',
            'code':'123456'
        }
        response = self.client.post(self.url,verify,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_email_verify_not_match_both(self):
        verify ={
            'email':'test2@test.com',
            'code':'654321'
        }
        response = self.client.post(self.url,verify,format='json')
        self.assertEqual(response.status_code,400)
        
class signUpTest(APITestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.verify_t = Verify.objects.create(email='test@test.com',code='123456',verification=True)
        self.verify_f = Verify.objects.create(email='test2@test.com',code='123456')
        self.user = User.objects.create_user(email='test3@test.com',password='12345678@', nickname='test2')
        
    def test_sign_up(self):
        user ={
            'email':'test@test.com',
            'password':'test1234@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,201)
        
    def test_sign_up_not_match_code(self):
        user ={
            'email':'test2@test.com',
            'password':'Test1234@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_sign_up_not_email(self):
        user ={
            'email':'test',
            'password':'Test1234@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_sign_up_not_include_lecture_in_password(self):
        user ={
            'email':'test',
            'password':'Test1234',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_sign_up_not_over_min_length_password(self):
        user ={
            'email':'test',
            'password':'Test12@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_sign_up_not_use_number_password(self):
        user ={
            'email':'test',
            'password':'testtest@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
        
    def test_sign_up_not_use_alphabat_password(self):
        user ={
            'email':'test',
            'password':'13245678@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_sign_up_overlapping_email(self):
        user ={
            'email':'test3@test.com',
            'password':'test1234@',
            'nickname':'test',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_sign_up_overlapping_nickname(self):
        user ={
            'email':'test3@test.com',
            'password':'test1234@',
            'nickname':'test2',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,400)
        
class loginTest(APITestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user_data = User.objects.create_user(email='test@test.com',password='qwer1234@', nickname='test')

    def test_login(self):
        user ={
            'email':'test@test.com',
            'password':'qwer1234@',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,200)
    
    def test_login_not_match_email(self):
        user ={
            'email':'test2@test.com',
            'password':'qwer1234@',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,401)
    
    def test_login_not_match_password(self):
        user ={
            'email':'test@test.com',
            'password':'12345678',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,401)
        
    def test_login_not_match_both(self):
        user ={
            'email':'test2@test.com',
            'password':'12345678',
        }
        response = self.client.post(self.url,user,format='json')
        self.assertEqual(response.status_code,401)

#alchol 북마크 기능 테스트
class BookmarkOfAlcholCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alchol_data = {
            'id':1,
            'name':'안동소주',
            'sort':'소주',
            'beverage':10.0,
            'taste':'깔끔한',
            }
        cls.user_data = {'id':1,"email": "test@test.com", "nickname":'test', "password": "test12!@"}
        cls.user = User.objects.create_user("test@test.com", 'test', 'test12!@', id=1)
        cls.alchol = Alchol.objects.create(**cls.alchol_data)

    def setUp(self):
        self.access_token = self.client.post(
            reverse("login"), self.user_data).data["access"]

    def test_alchol_bookmark(self):
        response = self.client.post(
            reverse('bookmark_view', kwargs={'alchol_id':self.alchol.id,}),
            marked_user_id=self.user.id,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            ) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': '북마크📌'})

    def test_alchol_bookmark_cancel(self):
        bookmark = BookMark.objects.create(marked_user_id=self.user.id, alchol_id=self.alchol.id)
        response = self.client.post(
            reverse('bookmark_view', kwargs={"alchol_id": self.alchol.id}),
            marked_user_id=self.user.id,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            ) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': '북마크📌 취소'})


#유저 팔로잉 기능 테스트
class FollowTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'id':1,"email": "test@test.com", "nickname":'test', "password": "test12!@"}
        cls.user_data2 = {'id':2,"email": "test2@test.com", "nickname":'test2', "password": "test12!@"}
        cls.user_data3 = {'id':3,"email": "test33@test.com", "nickname":'test33', "password": "test12!@"}

        cls.user = User.objects.create_user(id=1,email="test@test.com", nickname='test', password='test12!@')
        cls.user2 = User.objects.create_user(id=2,email="test2@test.com", nickname='test2', password='test12!@')

    def setUp(self):
        self.access_token = self.client.post(
            reverse("login"), self.user_data).data["access"]

    def test_followview_make_follow(self):
        response = self.client.post(
            reverse('follow', args=[self.user2.id,]),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            ) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': "팔로우"})

    def test_followview_cancel_follow(self):
        following_data = Follow.objects.create(follower_id=self.user.id, following_id=self.user2.id)
        response = self.client.post(
            reverse('follow', args=[self.user2.id,]),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            ) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message':"팔로우 취소"})

    def test_get_none_following_list(self):
        response = self.client.get(
            reverse('follow_user_view', kwargs={'follow_id':1,})
        )
        self.assertEqual(response.data, {'message': '아직 팔로우 정보가 없습니다.'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_following_list(self):
        user2_following_data = Follow.objects.create(id=1,follower_id=self.user2.id, following_id=self.user.id) # id = 3 !!

        response = self.client.get(
            reverse('follow_user_view', kwargs={'follow_id':1,})
        )
        self.assertEqual(Follow.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

