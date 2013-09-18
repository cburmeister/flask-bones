from flask import g
import app
import unittest
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from  sqlalchemy.sql.expression import func
from faker import Factory

fake = Factory.create()

admin_username = 'cburmeister'
admin_email = 'cburmeister@discogs.com'
admin_password = 'test123'

def make_db():
    db.drop_all()
    db.create_all()

    users = [User(admin_username,
        admin_email,
        admin_password,
        fake.ipv4())
    ]
    for _ in range(50):
        u = User(fake.userName(),
                fake.email(),
                fake.word(),
                fake.ipv4()
            )
        users.append(u)
    [db.session.add(x) for x in users]

    db.session.commit()


class TestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.app.test_client()
        make_db()

    def tearDown(self):
       make_db()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password,
            accept_tos=True
        ), follow_redirects=True)

    def create_user(self, username, email, password):
        return self.app.post('/user/create', data=dict(
            username=username,
            email=email,
            password=password,
            confirm=password
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

    def test_create_user(self):
        username = fake.userName()
        resp = self.login(admin_username, admin_password)
        resp = self.create_user(username, fake.email(), fake.word())
        assert 'User %s created' % username in resp.data

    def test_edit_user(self):
        user = User.query.order_by(func.random()).first()
        resp = self.login(admin_username, admin_password)
        resp = self.edit_user(user, email=fake.email())
        assert 'User %s edited' % user.username in resp.data

if __name__ == '__main__':
    unittest.main()
