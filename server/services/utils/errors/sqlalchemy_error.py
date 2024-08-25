from psycopg2 import errors

def handle_sqlalchemy_error(e):
    """Handle SQLAlchemy errors."""
    if isinstance(e.orig, errors.UndefinedTable):
        raise ValueError("Data does not exist") from e
    else:
        raise ValueError("Database error occurred") from e