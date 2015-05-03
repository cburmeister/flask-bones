from app import create_app, config
from app.database import db
from flask.ext.script import (
    Server,
    Shell,
    Manager,
    prompt_bool,
)
from tests import make_db


def _make_context():
    return dict(app=create_app(config.dev_config), db=db, make_db=make_db)


manager = Manager(create_app(config=config.dev_config))
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=_make_context))


@manager.command
@manager.option('-n', '--num_users', help='Number of users')
def create_db(num_users=5):
    """Creates database tables and populates them."""
    db.create_all()
    make_db(num_users=num_users)


@manager.command
def drop_db():
    """Drops database tables."""
    if prompt_bool('Are you sure?'):
        db.drop_all()


@manager.command
def recreate_db():
    """Same as running drop_db() and create_db()."""
    drop_db()
    create_db()


if __name__ == '__main__':
    manager.run()
