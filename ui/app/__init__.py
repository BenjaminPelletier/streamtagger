from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import jinja2

from .lib.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_environment.autoescape = jinja2.select_autoescape(['html', 'xml'])
app.jinja_env.globals.update(zip=zip)
app.jinja_env.globals.update(len=len)

dbx = SQLAlchemy(app)
migrate = Migrate(app, dbx)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
