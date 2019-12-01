from flask import Flask
import jinja2

app = Flask(__name__)
app.jinja_environment.autoescape = jinja2.select_autoescape(['html', 'xml'])
app.jinja_env.globals.update(zip=zip)
app.jinja_env.globals.update(len=len)

from app import routes
