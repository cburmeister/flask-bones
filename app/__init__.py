from flask import Flask, request, g
import time

app = Flask(__name__)

from app import views


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)
