from flask import request, redirect, url_for, render_template
from app import app, rules

@app.endpoint('index')
def index():
    return render_template('index.html')
