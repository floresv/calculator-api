from contextlib import contextmanager
from datetime import datetime
from flask import current_app
from sqlalchemy import exc

from ....api.common.utils.exceptions import ServerErrorException, \
    InvalidPayloadException, NotFoundException, \
    ValidationException


@contextmanager
def session_scope(session):
    """
    Provide a transactional scope around a series of operations.
    """
    try:
        yield session
        session.commit()
    except (InvalidPayloadException, NotFoundException,
            ValidationException) as e:
        session.rollback()
        raise e
    except exc.SQLAlchemyError:
        session.rollback()
        raise ServerErrorException()


def get_date(date: str) -> datetime:
    """
    Convert str to date in a specific format
    """
    return datetime.strptime(date, current_app.config.get('DATE_FORMAT'))


def get_date_str(date: datetime) -> str:
    """
    Convert date to str in a specific format
    """
    return date.strftime(current_app.config.get('DATE_FORMAT'))
