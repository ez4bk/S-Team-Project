from django.test import TestCase

from djangoProject.aes_pass import *
from djangoProject.models import *

aes_pass = AESCipher()


# test for model and databse connections
class models_tests(TestCase):
    # setup the test object
    def setUp(self):
        User.objects.create(user_name='test_account', password=aes_pass.encrypt_main('test_pw'), user_id='123')
        Children.objects.create(kids_name='Mike', time_limit=100, parent_id='123', icon_image='3')

    # test on get uer by username
    def test_get_user_by_name(self):
        users = User.objects.filter(user_id='123')
        user = users.first()
        decrypted_pw = aes_pass.decrypt_main(user.password)
        self.assertEqual(users.count(), 1)
        self.assertEqual(decrypted_pw, 'test_pw')
        self.assertEqual(user.user_id, '123')
        self.assertEqual(user.user_name, 'test_account')

    # test on get children by username
    def test_get_children_by_user(self):
        users = User.objects.filter(user_id='123')
        user = users.first()
        kids = Children.objects.filter(parent_id=user.user_id)
        kid = kids.first()
        self.assertEqual(users.count(), 1)
        self.assertEqual(kids.count(), 1)
        self.assertEqual(kid.time_limit, 100)
        self.assertEqual(kid.kids_name, 'Mike')
        self.assertEqual(kid.parent_id, '123')
        self.assertEqual(kid.icon_image, '3')

    # test on update timelimit by child name
    def test_update_timelimit(self):
        new_timelimit = 200
        kids = Children.objects.filter(parent_id='123', kids_name='Mike').update(time_limit=new_timelimit)
        kid = Children.objects.filter(parent_id='123', kids_name='Mike').first()
        self.assertEqual(kid.time_limit, new_timelimit)
