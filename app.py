from flask import Flask, jsonify
from flask_cors import CORS
from project import db, is_database_connected


def create_app():
    app = Flask(__name__)
    """Create and configure an instance of the Flask application."""
    app.config.from_prefixed_env()
    # app.config.from_mapping(
    #     # a default secret that should be overridden by instance config
    #     SECRET_KEY="dev",
    #     # store the database in the instance folder
    #     DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    # )
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    db.init_app(app)

    cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})

    from project.api.v1.auth import auth_blueprints
    from project.api.v1.user import user_blueprints
    from project.api.v1.record import record_blueprints

    # apply the blueprints to the app
    blueprints = [*auth_blueprints, *user_blueprints, *record_blueprints]
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix="/v1")

    return app


app = create_app()


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/status")
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


# register error handlers
from werkzeug.exceptions import HTTPException

from project.api.common.utils import exceptions
from project.api.common import error_handlers

app.register_error_handler(
    exceptions.InvalidPayloadException, error_handlers.handle_exception
)
app.register_error_handler(
    exceptions.BadRequestException, error_handlers.handle_exception
)
app.register_error_handler(
    exceptions.UnauthorizedException, error_handlers.handle_exception
)
app.register_error_handler(
    exceptions.ForbiddenException, error_handlers.handle_exception
)
app.register_error_handler(
    exceptions.NotFoundException, error_handlers.handle_exception
)
app.register_error_handler(
    exceptions.ServerErrorException, error_handlers.handle_exception
)
app.register_error_handler(Exception, error_handlers.handle_general_exception)
app.register_error_handler(HTTPException, error_handlers.handle_werkzeug_exception)
