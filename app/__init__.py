import flask, flask_sqlalchemy, flask_migrate, flask_login
from config import Config

app = flask.Flask(__name__)
app.config.from_object(Config)
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
login = flask_login.LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors
