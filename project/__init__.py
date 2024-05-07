import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .api.common.base_definitions import BaseFlask
from sqlalchemy import text

# flask config
# conf = Config(root_path=os.path.abspath(os.path.dirname(__file__)))
# conf.from_object(os.getenv('APP_SETTINGS'))

# instantiate the extensions
db = SQLAlchemy()


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_prefixed_env()
    # app.config.from_mapping(
    #     # a default secret that should be overridden by instance config
    #     SECRET_KEY="dev",
    #     # store the database in the instance folder
    #     DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    # )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from . import db

    db.init_app(app)

    # apply the blueprints to the app
    from .api.v1.auth import auth_blueprints
    from .api.v1.user import user_blueprints

    blueprints = [*auth_blueprints, *user_blueprints]
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix='/v1')

    # make url_for('index') == url_for('blog.index')
    # app.add_url_rule("/", endpoint="index")

    return app

def is_database_connected():
    """
    Attempts a connection to the database and returns True if successful.
    """
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.close()  # Close the cursor explicitly
            return True
    except Exception as e:
        print(f"Database connection error: {e}")
    return False

# register error handlers
from werkzeug.exceptions import HTTPException

from .api.common.utils import exceptions
from .api.common import error_handlers

app = create_app()

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/status')
def get_status():
    """
    Returns basic information about the API status.
    """
    status_data = {
        "message": "Calculator API is up and running!",
        "version": "0.0.1",
        "database_connected": is_database_connected(),
    }
    return jsonify(status_data)

app.register_error_handler(exceptions.InvalidPayloadException, error_handlers.handle_exception)
app.register_error_handler(exceptions.BadRequestException, error_handlers.handle_exception)
app.register_error_handler(exceptions.UnauthorizedException, error_handlers.handle_exception)
app.register_error_handler(exceptions.ForbiddenException, error_handlers.handle_exception)
app.register_error_handler(exceptions.NotFoundException, error_handlers.handle_exception)
app.register_error_handler(exceptions.ServerErrorException, error_handlers.handle_exception)
app.register_error_handler(Exception, error_handlers.handle_general_exception)
app.register_error_handler(HTTPException, error_handlers.handle_werkzeug_exception)


