import unittest
from app import create_app, db
from app.models import User
from helpers import signup, login, logout


class AuthTests(unittest.TestCase):


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


    def test_signup_confirm_login(self):

        # signup

        response = signup(self.client, "test@flaskask.xyz", "test", "12345")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Check your inbox" in response.get_data(as_text=True))

        # confirm account

        user = User.query.filter_by(email="test@flaskask.xyz").first()
        token = user.generate_confirmation_token()
        response = self.client.get("confirm/"+token, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have confirmed your account' in response.get_data(as_text=True))

        # login

        response = login(self.client, "test@flaskask.xyz", "12345")

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Questions' in response.get_data(as_text=True))

        # logout

        response = logout(self.client)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have been logged out' in response.get_data(as_text=True))


    def test_login_unconfirmed(self):

        # signup
        response = signup(self.client, "test@flaskask.xyz", "test", "12345")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Check your inbox" in response.get_data(as_text=True))

        # login unconfirmed
        response = login(self.client, "test@flaskask.xyz", "12345")

        self.assertEqual(response.status_code, 200)
        self.assertTrue('You need to confirm your account' in response.get_data(as_text=True))


    def test_login_failed(self):

        # login with unregistred account
        response = login(self.client, "test@flaskask.xyz", "12345")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid email or password" in response.get_data(as_text=True))


    def test_signup_email_existing(self):

        # signup
        response = signup(self.client, "test@flaskask.xyz", "test", "12345")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Check your inbox" in response.get_data(as_text=True))

        # signup again
        response = signup(self.client, "test@flaskask.xyz", "test", "12345")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Email already registered" in response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()