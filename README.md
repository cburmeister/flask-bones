![flasks](https://raw.githubusercontent.com/cburmeister/flask-bones/master/image.jpg)

flask-bones
===========

I've been reusing this pattern for Flask applications and decided to stop repeating myself.

## Setup

1. Install required services:

    ```
    $ brew install memcached
    $ brew install redis
    $ brew install postgresql
    $ gem install mailcatcher
    ```

2. Install Python packages:

    ```
    $ make init
    ```

3. Set necessary environment variables:

    ```
    $ export SECRET_KEY=46-2346-24986-2384632-2039845-24
    $ export DATABASE_URL=postgresql://$USER@localhost/flask_bones
    $ export SERVER_NAME=$HOST:5000
    ```

4. Install Javascript dependencies:

    ```
    $ make assets
    ```

5. Setup database and seed with test data:

    ```
    $ make db
    ```

6. Run a local SMTP server:

    ```
    $ mailcatcher
    ```

7. Run the celery worker:

    ```
    $ make celery
    ```

8. Run local server:

    ```
    $ make server
    ```

## Features

1. Caching with Memcached

    ```bash
    from app.extensions import cache

    # cache something
    cache.set('some_key', 'some_value')

    # fetch it later
    cache.get('some_key')
    ```

2. Email delivery

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
    from app.extensions import login_user, logout_user, login_required

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
    from app.extensions import bcrypt

    # hash password
    pw_hash = bcrypt.generate_password_hash('password')

    # validate password
    bcrypt.check_password_hash(pw_hash, 'password')
    ```

6. Easily swap between multiple application configurations

    ```bash
    from app.config import dev_config, test_config
    app = Flask(__name__)

    class dev_config():
        DEBUG = True

    class test_config():
        TESTING = True

    # configure for testing
    app.config.from_object(test_config)

    # configure for development
    app.config.from_object(dev_config)
    ```

7. Form validation & CSRF protection with WTForms

    ```bash
    # place a csrf token on a form
    {{ form.csrf_token }}

    # then validate
    form.validate_on_submit()
    ```

8. Scale with Blueprints

    ```bash
    # app/user/__init__.py
    user = Blueprint('user', __name__, template_folder='templates')

    # app/__init__.py
    app = Flask(__name__)
    app.register_blueprint(user, url_prefix='/user')
    ```

9. Automated tests

    ```bash
    # run the test suite
    python tests.py
    ```

10.  Use any relational database using the SQLAlchemy ORM

    ```bash
    from app.user.models import User

    # fetch user by id
    user = User.get_by_id(id)

    # save current state of user
    user.update()

    # fetch a paginated set of users
    users = User.query.paginate(page, 50)
    ```

11. Merge and compress your javascripts and stylesheets

    ```bash
    # create a bundle of assets
    js = Bundle(
        'js/jquery.js',
        'js/bootstrap.min.js',
        filters='jsmin',
        output='gen/packed.js'
    )
    ```

    ```bash
    # serve up a single minified file
    {% assets "js_all" %}
        <script type="text/javascript" src="{{ ASSET_URL }}"></script>
    {% endassets %}
    ```
