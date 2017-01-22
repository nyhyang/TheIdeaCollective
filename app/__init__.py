from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.login import current_user

app = Flask(__name__)
app.config.from_object('config')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
db.create_all()
app.secret_key = "p-jgtnRZMBMCPeve2uComf7x"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)

from app import views, models