from flask import Flask

app = Flask(__name__)

from kisseklyv import routes

app.run(port=5000)

