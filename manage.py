import coverage

from flask.cli import FlaskGroup

from project import app, db
from project.models.user import User

import unittest

cli = FlaskGroup(app)

COV = coverage.coverage(branch=True, include="project/*", omit=["project/static/*"])
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
    user1 = User(username="admin", password="password")
    user2 = User(username="user", password="password")
    db.session.add(user1)
    db.session.add(user2)
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
