"""
Initializing the application
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from quotesapi.utils import CreatureConverter, HumanConverter, AnimalConverter, QuoteConverter
from . import models
from . import api

db = SQLAlchemy()

# Based on http://flask.pocoo.org/docs/1.0/tutorial/factory/#the-application-factory
# Modified to use Flask SQLAlchemy
def create_app(test_config=None):
    """
    Creating and configuring the flask application instance.
    Initializes the database and registers components.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    #from . import models
    #from . import api
    #from quotesapi.utils import CreatureConverter, HumanConverter, AnimalConverter, QuoteConverter

    app.url_map.converters["creature"] = CreatureConverter
    app.url_map.converters["human"] = HumanConverter
    app.url_map.converters["animal"] = AnimalConverter
    app.url_map.converters["quote"] = QuoteConverter


    app.cli.add_command(models.init_db_command)
    app.register_blueprint(api.api_bp)
    return app
