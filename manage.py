import coverage

from flask.cli import FlaskGroup


from project.models.user import User
from project.models.operation import Operation
from project import db
import app

import unittest

cli = FlaskGroup(app)

COV = coverage.coverage(branch=True, include="project/*")
COV.start()


@cli.command("recreate_db")
def recreate_db() -> None:
    """
    Recreates the database
    """
    db.reflect()
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("create_db")
def create_db() -> None:
    """
    Create the database
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db() -> None:
    """
    Seed the database
    """
    user1 = User(username="admin", password="password", balance=10_000)
    user2 = User(username="user", password="password", balance=10_000)
    operation1 = Operation(type="addition", cost=10)
    operation2 = Operation(type="subtraction", cost=10)
    operation3 = Operation(type="multiplication", cost=10)
    operation4 = Operation(type="division", cost=10)
    operation5 = Operation(type="square_root", cost=10)
    operation6 = Operation(type="random_string", cost=10)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(operation1)
    db.session.add(operation2)
    db.session.add(operation3)
    db.session.add(operation4)
    db.session.add(operation5)
    db.session.add(operation6)
    db.session.commit()


@cli.command()
def cov() -> int:
    """
    Run the unit tests with coverage
    """
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == "__main__":
    cli()
