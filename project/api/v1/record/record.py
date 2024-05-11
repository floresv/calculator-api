from flask import request, current_app, jsonify, Blueprint

from ..base import token_required
from ....models.record import Record
from ....models.operation import Operation
from ...common.utils.exceptions import (
    NotImplementedException,
    NotFoundException,
    BadRequestException,
)
from .... import db
from project.calculator import Calculator

bp = Blueprint("record", __name__)


@bp.route("/records", methods=["POST"])
@token_required
def add(current_user):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing params"}), 400
    if not data or not data.get("first_value"):
        return jsonify({"error": "Missing numbers"}), 400
    if not data.get("operation"):
        return jsonify({"error": "Missing operation"}), 400

    if data.get("second_value"):
        num2 = data["second_value"]
    else:
        num2 = None
    num1 = data["first_value"]
    operation = Operation.query.filter_by(type=data["operation"]).first()
    if not operation:
        return jsonify({"error": "Invalid operation"}), 400
    if current_user.get_balance() < operation.cost:
        return jsonify({"error": "Insufficient balance"}), 400

    try:
        # Flask-SQLAlchemy automatically start a transaction within the request context.
        try:
            current_user.charge_operation(operation=operation)
            result = Calculator().operation(
                first_value=num1, second_value=num2, operation=operation.type
            )
            record = current_user.add_record(operation=operation, result=result)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e  # Re-raise the exception to propagate it
        current_app.logger.info(f"Record added successfully")
        return jsonify({"record": record.json()}), 200
    except TypeError:
        return jsonify({"error": "Invalid data types"}), 400
    except NotImplementedException:
        return jsonify({"error": "Operation not implemented"}), 400
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 400


@bp.route("/records", methods=["GET"])
@token_required
def get_list(current_user):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    sort_by = request.args.get("sort_by", "id", type=str)
    sort_order = request.args.get("sort_order", "asc", type=str)
    operation_type = request.args.get("filter_by_operation_type", None, type=str)
    amount = request.args.get("filter_by_amount", None, type=float)
    user_balance = request.args.get("filter_by_user_balance", None, type=float)
    operation_response = request.args.get(
        "filter_by_operation_response", None, type=str
    )

    try:
        records = current_user.records_non_deleted(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            amount=amount,
            operation_type=operation_type,
            user_balance=user_balance,
            operation_response=operation_response,
        )
    except Exception as e:
        return BadRequestException(message=str(e)).to_dict(), 400
    data = {
        "records": [record.json() for record in records.items],
        "total": records.total,
        "pages": records.pages,
        "current_page": records.page,
        "per_page": per_page,
        "next_page": records.next_num,
        "prev_page": records.prev_num,
        "has_next": records.has_next,
        "has_prev": records.has_prev,
        "sort_by": sort_by,
        "sort_order": sort_order,
    }
    return jsonify(data), 200


@bp.route("/records/<int:record_id>", methods=["DELETE"])
@token_required
def delete_record(current_user, record_id):
    record = Record.first_by(id=record_id, user_id=current_user.id)
    if not record:
        raise NotFoundException("Record not found")
    record.delete()
    return jsonify({"message": "Record deleted successfully"}), 200
