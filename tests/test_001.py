import unittest
from flask import current_app
from app import create_app, db
from app.models import User, Question, UserQuestion, Option, File


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_create_user(self):
        user = User()
        user.from_dict(
            {'first_name': 'fred', 'last_name': 'flint', 'email': 'fred@flint.com'})
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.get_username(), 'Fred Flint',
                         "User.get_username is correct")
        user_same_email = User()
        user_same_email.from_dict(
            {'first_name': 'almost', 'last_name': 'same', 'email': 'fred@flint.com'})
        with self.assertRaises(Exception, msg="Cannot create another user with the same email."):
            db.session.add(user_same_email)
            db.session.commit()

    def test_user_token(self):
        user = User()
        user.from_dict(
            {'first_name': 'new', 'last_name': 'user', 'email': 'new@user.com'})
        db.session.add(user)
        db.session.commit()
        user_token = user.create_reset_token(10)
        self.assertEqual(len(user_token), 32, "User token is ok")
        verified_user = user.verify_user_token(user_token)

        self.assertTrue((user.get_username() == verified_user.get_username()) and
                        (user.email == verified_user.email),  "Token verification returns the correct user")

        user.remove_token()
        user_token = user.get_token()
        self.assertIs(user_token, None, "User token was forcibly expired")
