from flask import request, redirect, url_for, render_template
from app import app, rules
from models import User

@app.endpoint('index')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)
