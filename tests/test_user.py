import unittest
from app import create_app, db
from app.models import User

class UserModelTests(unittest.TestCase):


    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_password_setter(self):
        user = User(password='12345')
        self.assertTrue(user.password_hash is not None)


    def test_password_getter(self):
        user = User(password='12345')
        with self.assertRaises(AttributeError):
            user.password


    def test_valid_confirmation_token(self):
        user = User(password='12345')
        token = user.generate_confirmation_token()
        self.assertTrue(user.confirm(token))


    def test_invalid_confirmation_token(self):
        user = User(password='12345')
        self.assertFalse(user.confirm('abcdefg'))
