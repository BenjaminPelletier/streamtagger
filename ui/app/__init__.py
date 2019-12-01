from flask import Flask

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.jinja_env.globals.update(len=len)

from app import routes
