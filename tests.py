from flask import g
import app
import unittest
from app import db
from app.models import User, Permission


class TestCase(unittest.TestCase):

    def make_db(self):
        db.drop_all()
        db.create_all()

        users = [
            User('cburmeister', 'burmeister.corey@gmail.com', 'test123'),
            User('dbolt', 'junglist88@gmail.com', 'test123'),
            User('abihner', 'senamoru@gmail.com', 'test123'),
            User('ekroll', 'djkrypplephite@gmail.com', 'test123')
        ]
        [db.session.add(x) for x in users]

        permissions = [
            Permission('admin', 1),
            Permission('create_user', 1),
            Permission('admin', 2),
        ]
        [db.session.add(x) for x in permissions]

        db.session.commit()

    def setUp(self):
        self.app = app.app.test_client()
        self.make_db()

    def tearDown(self):
        self.make_db()
        
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def create_user(self, username, email, password):
        return self.app.post('/create_user', data=dict(
            username=username,
            email=email,
            password=password
        ), follow_redirects=True)

    def test_login(self):
        resp = self.login('cburmeister', 'test123')
        assert 'You were logged in' in resp.data

    def test_logout(self):
        resp = self.login('cburmeister', 'test123')
        assert 'You were logged in' in resp.data
        resp = self.app.get('/logout', follow_redirects=True)
        assert 'You were logged out' in resp.data

    def test_create_user(self):
        username = 'jrogen'

        # test user without permission
        resp = self.login('dbolt', 'test123')
        resp = self.app.get('/create_user')
        assert 401 == resp.status_code

        # test user with permission
        resp = self.create_user(username, 'j.rogen@gmail.com', 'test123')
        resp = self.login('cburmeister', 'test123')
        resp = self.create_user(username, 'j.rogen@gmail.com', 'test123')
        assert 'User %s created' % username in resp.data

if __name__ == '__main__':
    unittest.main()
