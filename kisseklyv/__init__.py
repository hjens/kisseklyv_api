from flask import Flask
import config
import flask_sqlalchemy
import flask_migrate

app = Flask(__name__)
app.config.from_object(config.Config())
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

from kisseklyv import resources, models

if __name__ == '__main__':
    app.run(port=5000)