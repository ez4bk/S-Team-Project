from django.test import TestCase
from django.test import Client
from djangoProject.views import *
from django.shortcuts import render, HttpResponse, redirect
from djangoProject.models import *
from djangoProject.aes_pass import *
from django.contrib import messages

aes_pass = AESCipher()

# class models_tests(TestCase):
#     def setUp(self):
#         c = Client()
#         response = c.post('/login/', {'user_id': 'john', 'password': 'smith'})
#         response.status_code
