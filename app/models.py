from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer(),
            db.ForeignKey('user.id', ondelete="CASCADE"))
    user = db.relationship('User', 
            backref=db.backref('permissions', lazy='dynamic'))

    def __init__(self, desc, user_id):
        self.desc = desc
        self.user_id = user_id

    def __repr__(self):
        return '<Permission %r>' % self.desc
