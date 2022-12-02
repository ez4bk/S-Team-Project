from django.test import TestCase
from django.test import Client, RequestFactory
from djangoProject.views import *
from django.shortcuts import render, HttpResponse, redirect
from djangoProject.models import *
from djangoProject.aes_pass import *
from django.contrib import messages

aes_pass = AESCipher()


class views_tests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(user_name='test_account', password=aes_pass.encrypt_main('test_pw'), user_id='123')
        Children.objects.create(kids_name='Mike', time_limit=100, parent_id='123', icon_image='3')

    def test_login_page(self):
        request = self.factory.get('login/')
        request.user = self.user
        response = sign(request)
        self.assertEqual(response.status_code, 200)

    # def test_login_post(self):
    #     # request = self.factory.post('login/', {'user_id': 123, 'password': 'test_pw'})
    #     # request.user = self.user
    #     # request.session['user_id'] = ''
    #     # response = sign(request)
    #     c = Client()
    #     # response = c.post('login/', {'user_id': 123, 'password': 'test_pw'})
    #     response = self.client.post('login/', {'user_id': 123, 'password': 'test_pw'})
    #     print(response.status_code)
