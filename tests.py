from flask import g
from app import create_app
from app.config import test_config
from app.database import db
from app.user.models import User
from  sqlalchemy.sql.expression import func
from faker import Factory
import unittest

fake = Factory.create()

admin_username = 'cburmeister'
admin_email = 'cburmeister@discogs.com'
admin_password = 'test123'


def make_db():
    db.drop_all()
    db.create_all()

    users = [
        User(admin_username,
            admin_email,
            admin_password,
            fake.ipv4(),
            active=True,
            is_admin=True
        )
    ]
    for _ in range(5):
        u = User(
            fake.userName(),
            fake.email(),
            fake.word() + fake.word(),
            fake.ipv4()
        )
        users.append(u)
    [db.session.add(x) for x in users]

    db.session.commit()


class TestCase(unittest.TestCase):
    def setUp(self):
        app = create_app(test_config)
        db.app = app # hack for using db.init_app(app) in app/__init__.py
        self.app = app.test_client()
        make_db()

    def tearDown(self):
       make_db()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def register_user(self, username, email, password):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm=password,
            accept_tos=True
        ), follow_redirects=True)

    def edit_user(self, user, email):
        return self.app.post('/user/edit/%s' % user.id, data=dict(
            username=user.username,
            email=user.email,
        ), follow_redirects=True)

    def test_login(self):
        resp = self.login(admin_username, admin_password)
        assert 'You were logged in' in resp.data

    def test_logout(self):
        resp = self.login(admin_username, admin_password)
        assert 'You were logged in' in resp.data
        resp = self.app.get('/logout', follow_redirects=True)
        assert 'You were logged out' in resp.data

    def test_register_user(self):
        username = fake.userName()
        email = fake.email()
        password = fake.word() + fake.word()
        resp = self.register_user(username, email, password)
        assert 'Sent verification email to %s' % email in resp.data

    def test_edit_user(self):
        user = User.query.order_by(func.random()).first()
        resp = self.login(admin_username, admin_password)
        resp = self.edit_user(user, email=fake.email())
        assert 'User %s edited' % user.username in resp.data


if __name__ == '__main__':
    unittest.main()
