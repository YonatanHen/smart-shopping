from sqlalchemy.orm import sessionmaker
from DB.PsqlConnection import engine

def get_session():
    """Create an return new DB session"""
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    return session