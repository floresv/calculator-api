import datetime
import os
import logging
from json import JSONEncoder
from flask import Flask, jsonify, Response
from flask_cors import CORS


class BaseJSONEncoder(JSONEncoder):
    """
    Encodes JSON
    """

    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class BaseResponse(Response):
    """
    Base response
    """

    default_mimetype = "application/json"

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(BaseResponse, cls).force_type(rv, environ)


class BaseFlask(Flask):
    """
    Construct base application module
    """

    response_class = BaseResponse
    # set up custom encoder to handle date as ISO8601 format
    json_encoder = BaseJSONEncoder

    def __init__(self, import_name):
        Flask.__init__(
            self, import_name, static_folder="./static", template_folder="./templates"
        )
        # set config
        app_settings = os.getenv("APP_SETTINGS")
        self.config.from_object(app_settings)

        ##
        # configure logging
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            self.config["LOGGING_LOCATION"], "a", 1 * 1024 * 1024, 10
        )
        file_handler.setFormatter(logging.Formatter(self.config["LOGGING_FORMAT"]))
        self.logger.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)

        # enable CORS
        CORS(self)
