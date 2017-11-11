![flasks](https://raw.githubusercontent.com/cburmeister/flask-bones/master/image.jpg)

flask-bones
===========

An example of a large scale Flask application using blueprints and extensions.

## Setup

Quickly run the project using [docker](https://www.docker.com/) and
[docker-compose](https://docs.docker.com/compose/):
```bash
docker-compose up -d
```

Create the database and seed it with some data:
```bash
docker-compose run --rm app flask create_db
docker-compose run --rm app flask populate_db --num_users 5
```

Download front-end dependencies with [yarn](https://yarnpkg.com/en/):
```bash
yarn install --modules-folder ./app/static/node_modules
```

## Features

### Caching with Memcached

```python
from app.extensions import cache

# Cache something
cache.set('some_key', 'some_value')

# Fetch it later
cache.get('some_key')
```

### Email delivery

```python
from app.extensions import mail
from flask_mail import Message

# Build an email
msg = Message('User Registration', sender='admin@flask-bones.com', recipients=[user.email])
msg.body = render_template('mail/registration.mail', user=user, token=token)

# Send
mail.send(msg)
```

### Asynchronous job scheduling with RQ

`RQ` is a [simple job queue](http://python-rq.org/) for python backed by
[redis](https://redis.io/).

Define a job:
```python
@rq.job
def send_email(msg):
    mail.send(msg)
```

Start a worker:
```bash
flask rq worker
```

Queue the job for processing:
```python
send_email.queue(msg)
```

Monitor the status of the queue:
```bash
flask rq info --interval 3
```

For help on all available commands:
```bash
flask rq --help
```

### Stupid simple user management

```python
from app.extensions import login_user, logout_user, login_required

# Login user
login_user(user)

# You now have a global proxy for the user
current_user.is_authenticated

# Secure endpoints with a decorator
@login_required

# Log out user
logout_user()
```

### Password security that can keep up with Moores Law

```python
from app.extensions import bcrypt

# Hash password
pw_hash = bcrypt.generate_password_hash('password')

# Validate password
bcrypt.check_password_hash(pw_hash, 'password')
```

### Easily swap between multiple application configurations

```python
from app.config import dev_config, test_config

app = Flask(__name__)

class dev_config():
    DEBUG = True

class test_config():
    TESTING = True

# Configure for testing
app.config.from_object(test_config)

# Configure for development
app.config.from_object(dev_config)
```

### Form validation & CSRF protection with WTForms

Place a csrf token on a form:
```html
{{ form.csrf_token }}
```

Validate it:
```python
form.validate_on_submit()
```

### Automated tests

Run the test suite:
```bash
pytest
```

### Use any relational database using the SQLAlchemy ORM

```python
from app.user.models import User

# Fetch user by id
user = User.get_by_id(id)

# Save current state of user
user.update()

# Fetch a paginated set of users
users = User.query.paginate(page, 50)
```

### Front-end asset management

Download front-end dependencies with [yarn](https://yarnpkg.com/en/):
```bash
yarn install --modules-folder ./app/static/node_modules
```

Merge and compress them together with
[Flask-Assets](https://flask-assets.readthedocs.io/en/latest/):
```bash
flask assets build
```

### Version your database schema

Display the current revision:
```bash
flask db current
```

Create a new migration:
```bash
flask db revision
```

Upgrade the database to a later version:
```bash
flask db upgrade
```

### Internationalize the application for other languages (i18n)

Extract strings from source and compile a catalog (`.pot`):
```bash
pybabel extract -F babel.cfg -o i18n/messages.pot .
```

Create a new resource (.po) for German translators:
```bash
pybabel init -i i81n/messages.pot -d i18n -l de
```

Compile translations (.mo):
```bash
pybabel compile -d i18n
```

Merge changes into resource files:
```bash
pybabel update -i i18n/messages.pot -d i18n
```
