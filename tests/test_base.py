import unittest
from app import create_app, db


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_db_exists(self):
        self.assertFalse(db is None)

    def test_admin_exists(self):
        self.assertFalse(self.app.config['ADMIN_EMAIL'] is None)
