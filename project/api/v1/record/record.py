from flask import request, current_app, jsonify, Blueprint

from ..base import token_required
from ....models.user import Record
from ...common.utils.exceptions import NotImplementedException
from .... import db
from project.calculator import Calculator

bp = Blueprint("record", __name__)


@bp.route('/records', methods=['POST'])
# @token_required
# def add(current_user):
def add():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing params'}), 400
    if not data or not data.get('first_value') or not data.get('second_value'):
        return jsonify({'error': 'Missing numbers'}), 400
    if not data.get('operation'):
        return jsonify({'error': 'Missing operation'}), 400

    num1 = data['first_value']
    num2 = data['second_value']
    operation = data['operation']

    try:
        result = Calculator().operation(first_value=num1, second_value=num2, operation=operation)
        return jsonify({'result': result}), 200
    except TypeError:
        return jsonify({'error': 'Invalid data types'}), 400
    except NotImplementedException:
        return jsonify({'error': 'Operation not implemented'}), 400
