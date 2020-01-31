import flask
import flask_restful
import config
import flask_sqlalchemy
import flask_migrate

app = flask.Flask(__name__)
app.config.from_object(config.Config())
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
api = flask_restful.Api(app)

from kisseklyv import resources, models

api.add_resource(resources.KisseResource, "/kisse")

if __name__ == '__main__':
    app.run(port=5000)