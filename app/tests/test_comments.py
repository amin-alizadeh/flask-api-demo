import unittest

from flask import json
from app import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:g&yTSwhHJ5@localhost/ta-db-test"
    API_KEY_SECRET = "your_master_secret"


class TestComments(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_comment(self):
        with self.app.test_client() as c:

            feedback_payload = {"feedback": "This is a test feedback"}

            resp = c.post(
                "/api/comments",
                headers={"secret": self.app.config["API_KEY_SECRET"]},
                json=feedback_payload,
            )

            comment_payload = {"feedback": "This is a test comment"}

            c.post(
                "/api/comments",
                headers={"secret": self.app.config["API_KEY_SECRET"]},
                json=comment_payload,
            )

            resp = c.get(
                "/api/comments/1",
                headers={"secret": self.app.config["API_KEY_SECRET"]},
            )

            json_data = resp.get_json()

            self.assertEqual(200, resp.status_code, msg=json_data)

    
if __name__ == "__main__":
    unittest.main()
