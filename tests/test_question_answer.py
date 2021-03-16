import unittest
from app import create_app, db
from helpers import signup, login

class QuestionAnswerTests(unittest.TestCase):


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


    def test_question_answer(self):

        response = signup(self.client, "test@flaskask.xyz", "test", "12345")
        self.assertTrue(response.status_code, 200)

        response = login(self.client, "test@flaskask.xyz", "12345")
        self.assertTrue(response.status_code, 200)

        response = self.client.post('/new_question',
                            data={
                                    'title': "Just a simple title",
                                    'body': "Just a simple body"
                            }, follow_redirects=True)

        self.assertTrue("Just a simple title" in response.get_data(as_text=True))

        response = self.client.post('/question/1',
                            data={
                                    'body': "Just a simple answer"
                            }, follow_redirects=True)

        self.assertTrue("Just a simple answer" in response.get_data(as_text=True))

        response = self.client.post('/delete_answer/1', follow_redirects=True)
        self.assertTrue("Just a simple answer" not in response.get_data(as_text=True))

        response = self.client.post('/delete_question/1', follow_redirects=True)
        self.assertTrue("Just a simple title" not in response.get_data(as_text=True))


