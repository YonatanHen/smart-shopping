from sqlalchemy.orm import sessionmaker

def get_session():
    """Create an return new DB session"""
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()