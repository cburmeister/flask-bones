import app
import unittest
from app import db
from app.models import User

class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

        db.create_all()

        users = [
            User('cburmeister', 'burmeister.corey@gmail.com'),
            User('dbolt', 'junglist88@gmail.com'),
            User('abihner', 'senamoru@gmail.com'),
            User('hmarshall', 'herbmarshall@gmail.com'),
            User('ekroll', 'djkrypplephite@gmail.com')
        ]

        for u in users:
            db.session.add(u)

        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_index(self):
        resp = self.app.get('/')
        assert 'cburmeister' in resp.data

if __name__ == '__main__':
    unittest.main()
