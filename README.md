flask-bones
===========

[![Build Status](https://travis-ci.org/cburmeister/flask-bones.png?branch=master)](https://travis-ci.org/cburmeister/flask-bones)
[![Coverage Status](https://coveralls.io/repos/cburmeister/flask-bones/badge.png?branch=master)](https://coveralls.io/r/cburmeister/flask-bones?branch=master)

I've been reusing this pattern for Flask applications and decided to stop repeating myself.

## 

1. Caching with Memcached

    ```bash
    from app import cache

    # cache something
    cache.set('some_key', 'some_value')

    # fetch it later
    cache.get('some_key')
    ```

2. Email delivery with Mailgun

    ```bash
    from app.extensions import mail
    from flask.ext.mail import Message

    # build an email
    msg = Message('User Registration', sender='admin@flask-bones.com', recipients=[user.email])
    msg.body = render_template('mail/registration.mail', user=user, token=token)

    # send
    mail.send(msg)
    ```

3. Asynchronous job scheduling with Celery & Redis

    ```bash
    from app.extensions import celery

    # define a job
    @celery.task                                                                     
    def send_email(msg):                                                             
        mail.send(msg) 

    # queue job
    send_email.delay(msg)
    ```

4. Stupid simple user management

    ```bash
    from app.extensions import

    # login user
    login_user(user)

    # you now have a global proxy for the user
    current_user.is_authenticated

    # secure endpoints with a decorator
    @login_required

    # log out user
    logout_user()
    ```

5. Password security that can keep up with Moores Law

    ```bash
    # hash password
    pw_hash = bcrypt.generate_password_hash('password')

    # validate password
    bcrypt.check_password_hash(pw_hash, 'password')
    ```

6. Deploy on Heroku with ease

    ```bash
    # provision new stack
    $ heroku create

    # configure environment
    $ heroku config

    # deploy
    $ git push heroku master
    ```

7. Easily swap between multiple application configurations

    ```bash
    from app.config import dev_config, test_config
    app = Flask(__name__)

    # configure for testing
    app.config.from_object(test_config)

    # configure for development
    app.config.from_object(dev_config)
    ```

8. Form validation & CSRF protection with WTForms

    ```bash
    # place a csrf token on a form
    {{ form.csrf_token }}

    # then validate
    form.validate_on_submit()
    ```

10. Scale with Blueprints

    ```bash
    # app/user/__init__.py
    user = Blueprint('user', __name__, template_folder='templates')

    # app/__init__.py
    app = Flask(__name__)
    app.register_blueprint(user, url_prefix='/user')
    ```

11. Automated tests and continuous integration support for TravisCI

    ```bash
    # run the test suite
    python tests.py

    #from travis.yml
    coverage run tests.py
    ```

    ```bash
    # load the database with test data 
    from tests import make_db
    make_db()
    ```

12.  Use any relational database using the SQLAlchemy ORM

    ```bash
    # fetch user by id
    user = User.get_by_id(id)

    # save current state of user
    user.update()

    # fetch a paginated set of users
    users = User.query.paginate(page, 50)
    ```
