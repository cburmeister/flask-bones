from flask_login import UserMixin
from app.extensions import cache, bcrypt
from app.database import db, CRUDMixin
import datetime


class User(CRUDMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    pw_hash = db.Column(db.String(60), nullable=False)
    created_ts = db.Column(db.DateTime(timezone=True),
            server_default=db.func.current_timestamp(),)
    updated_ts = db.Column(db.DateTime(timezone=True),
            onupdate=db.func.current_timestamp(),)
    remote_addr = db.Column(db.String(20))
    active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean())

    def __init__(self, username, email, password, remote_addr, active=False, is_admin=False):
        self.username = username
        self.email = email
        self.set_password(password)
        self.created_ts = datetime.datetime.now()
        self.remote_addr = remote_addr
        self.active = active
        self.is_admin = is_admin

    def __repr__(self):
        return '<User %s>' % self.username

    def set_password(self, password):
        self.pw_hash = bcrypt.generate_password_hash(password, 10)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)

    @classmethod
    def stats(cls):
        active_users = cache.get('active_users')
        if not active_users:
            active_users = cls.query.filter_by(active=True).count()
            cache.set('active_users', active_users)

        inactive_users = cache.get('inactive_users')
        if not inactive_users:
            inactive_users = cls.query.filter_by(active=False).count()
            cache.set('inactive_users', inactive_users)

        return {
            'all': active_users + inactive_users,
            'active': active_users,
            'inactive': inactive_users
        }
