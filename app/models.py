from app import db
from sqlalchemy.orm import exc
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import abort


user_permissions = db.Table('user_permissions',
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    pw_hash = db.Column(db.String(80), nullable=False)

    permissions = db.relationship('Permission', secondary=user_permissions, 
            backref=db.backref('permissions', lazy='dynamic'))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(80), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('permission.id'))

    def __init__(self, desc, master_id=None):
        self.desc = desc
        self.master_id = master_id

    def __repr__(self):
        return '<Permission %s %s>' % (self.desc, self.master_id)
