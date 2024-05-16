from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# instantiate the extensions
db = SQLAlchemy()


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
