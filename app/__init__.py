from flask import Flask

# import configuration documents
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# add config info
app.config.from_object(Config)
# connect to db
db = SQLAlchemy(app)
# bind app with db
migrate = Migrate(app, db)

