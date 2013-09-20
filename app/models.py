from flask.ext.login import UserMixin
from app.database import CRUDMixin, db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(CRUDMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    pw_hash = db.Column(db.String(80), nullable=False)
    created_ts = db.Column(db.DateTime(), nullable=False)
    remote_addr = db.Column(db.String(20))
    sudo = db.Column(db.Boolean())

    def __init__(self, username, email, password, remote_addr):
        self.username = username
        self.email = email
        self.set_password(password)
        self.created_ts = datetime.datetime.now()
        self.remote_addr = remote_addr
        self.sudo = False

    def __repr__(self):
        return '<User %s>' % self.username

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
