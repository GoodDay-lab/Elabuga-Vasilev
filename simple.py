from flask import Flask
from data import db_session
import api


app = Flask(__name__)


def main(port):
    db_session.global_init("/db/blogs.sqlite")
    app.register_blueprint(api.blueprint)
    app.run(port=port)
    

main(7000)
