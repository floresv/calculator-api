from flask import request, current_app, jsonify, Blueprint

from ..base import token_required
from ....models.record import Record
from ....models.operation import Operation
from ...common.utils.exceptions import NotImplementedException
from .... import db
from project.calculator import Calculator

bp = Blueprint("record", __name__)


@bp.route('/records', methods=['POST'])
@token_required
def add(current_user):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing params'}), 400
    if not data or not data.get('first_value'):
        return jsonify({'error': 'Missing numbers'}), 400
    if not data.get('operation'):
        return jsonify({'error': 'Missing operation'}), 400

    if data.get('second_value'):
        num2 = data['second_value']
    else:
        num2 = None
    num1 = data['first_value']
    operation = Operation.query.filter_by(type=data['operation']).first()
    if not operation:
        return jsonify({'error': 'Invalid operation'}), 400
    if current_user.get_balance() < operation.cost:
        return jsonify({'error': 'Insufficient balance'}), 400

    try:
        current_user.charge_operation(operation=operation)
        result = Calculator().operation(first_value=num1, second_value=num2, operation=operation.type)
        current_user.add_record(operation=operation, result=result)
        db.session.commit()
        current_app.logger.info(f'Record added successfully')
        return jsonify({'result': result}), 200
    except TypeError:
        return jsonify({'error': 'Invalid data types'}), 400
    except NotImplementedException:
        return jsonify({'error': 'Operation not implemented'}), 400


@bp.route("/records", methods=['GET'])
@token_required
def get_list(current_user):
    records = current_user.records
    return jsonify({"records": [record.json() for record in records]}), 200
