from flask.ext.script import Server, Shell, Manager
from app import create_app
from app.database import db
from app import config
from tests import make_db


def _make_context():
    return dict(app=create_app(config.dev_config), db=db, make_db=make_db)


manager = Manager(create_app(config=config.dev_config))
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=_make_context))


if __name__ == '__main__':
    manager.run()
