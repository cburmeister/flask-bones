import os
import app
import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        resp = self.app.get('/')
        assert 'Hello World!' in resp.data

if __name__ == '__main__':
    unittest.main()
