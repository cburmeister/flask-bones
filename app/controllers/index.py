from flask import request, redirect, url_for
from app import app, rules


@app.endpoint('index')
def display(self):
    self.render_template()
