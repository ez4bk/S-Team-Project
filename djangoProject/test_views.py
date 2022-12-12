from django.test import TestCase
from django.test import RequestFactory
from djangoProject.views import *
from djangoProject.models import *
from djangoProject.aes_pass import *
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

aes_pass = AESCipher()


# test for view functions
class views_tests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.get('/')
        self.session = SessionMiddleware(request)
        self.message = MessageMiddleware(request)
        self.user = User.objects.create(user_name='test_account', password=aes_pass.encrypt_main('test_pw'),
                                        user_id='123')

    # test for get function in login
    def test_login_page_get(self):
        request = self.factory.get('login/')
        request.user = self.user
        response = sign(request)
        self.assertEqual(response.status_code, 200)

    # test for post function in login
    def test_login_post(self):
        request = self.factory.post('signin/',
                                    {'user_id': '123',
                                     'password': 'test_pw'})
        request.user = self.user
        self.session.process_request(request)
        request.session.save()
        response = sign(request)
        self.assertEqual(response.cookies['id'].value, '123')
        self.assertEqual(response.status_code, 302)

        request = self.factory.post('signin/', {'user_id': '123'})
        request.user = self.user
        self.session.process_request(request)
        self.message.process_request(request)
        request.session.save()
        response = sign(request)
        self.assertIsNone(response.cookies.get('id'))
        self.assertEqual(response.status_code, 302)

        request = self.factory.post('signin/',
                                    {'user_id': '123',
                                     'password': 'test_pw_wrong'})
        request.user = self.user
        self.session.process_request(request)
        self.message.process_request(request)
        request.session.save()
        response = sign(request)
        self.assertIsNone(response.cookies.get('id'))
        self.assertEqual(response.status_code, 302)

    # test for get function in register
    def test_register_get(self):
        request = self.factory.get('register/')
        request.user = self.user
        response = register(request)
        self.assertEqual(response.status_code, 200)
        request = self.factory.get('register/')
        response = register(request)
        self.assertEqual(response.status_code, 200)

    # test for post function in register
    def test_register_post(self):
        request = self.factory.post('register/',
                                    {'user_id': '321',
                                     'password': 'test_pw1',
                                     'username': 'test_account1'})
        self.session.process_request(request)
        request.session.save()
        response = register(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.cookies['id'].value, '321')

        request = self.factory.post('register/', {'user_id': self.user.user_id,
                                                  'password': 'test_pw_wrong'})
        self.session.process_request(request)
        self.message.process_request(request)
        request.session.save()
        response = register(request)
        self.assertIsNone(response.cookies.get('id'), 302)
        self.assertEqual(response.status_code, 302)

    # test for logout
    def test_logout(self):
        request = self.factory.get('logout/')
        request.user = self.user
        self.session.process_request(request)
        request.session['id'] = self.user.user_id
        request.session.save()
        request.COOKIES['id'] = self.user.user_id
        response = logout(request)
        self.assertEqual(response.status_code, 302)

    # test for get function in my children
    def test_my_children_get(self):
        request = self.factory.get('logout/')
        self.session.process_request(request)
        self.message.process_request(request)
        request.session.save()
        request.user = self.user
        Children.objects.create(kids_name='Mike', time_limit=100, parent_id='123', icon_image='3')
        response = my_children(request)
        self.assertEqual(response.status_code, 200)

    # test for post function in my children
    def test_my_children_post(self):
        request = self.factory.post('logout/', {'Mike': '20', 'Mikehours': '1'})
        self.session.process_request(request)
        self.message.process_request(request)
        request.session.save()
        request.user = self.user
        Children.objects.create(kids_name='Mike', time_limit=100, parent_id='123', icon_image='3')
        response = my_children(request)
        self.assertEqual(response.status_code, 200)

    # test for my profile
    def test_my_profile(self):
        request = self.factory.get('my_profile/')
        request.user = self.user
        self.session.process_request(request)
        request.session['user_id'] = self.user.user_id
        request.session.save()
        response = my_profile(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get('my_profile/')
        self.session.process_request(request)
        request.session.save()
        response = my_profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Could not get user information')

    # test for about us page
    def test_about_us(self):
        request = self.factory.get('my_profile/')
        request.user = self.user
        response = about_us(request)
        self.assertEqual(response.status_code, 200)

    # test for main page
    def test_page(self):
        request = self.factory.get('')
        request.user = self.user
        self.session.process_request(request)
        request.session['user_id'] = self.user.user_id
        self.message.process_request(request)
        request.session.save()
        response = page(request)
        self.assertEqual(response.status_code, 200)
