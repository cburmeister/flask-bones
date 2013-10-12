from app.extensions import celery, mail
from app.database import db
from flask.globals import current_app
from celery.signals import task_postrun


@celery.task
def send_registration_email(user, token):
    msg = Message('User Registration', sender='admin@flask-bones.com', recipients=[user.email])
    msg.body = render_template('mail/registration.mail', user=user, token=token)
    mail.send(msg)


@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from 
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors 
    # won't propagate across tasks)
    db.session.remove()
