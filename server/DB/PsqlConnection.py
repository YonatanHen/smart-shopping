import os
from sqlalchemy import create_engine
from models import Base

PSQL_USERNAME=os.environ.get('PSQL_USERNAME')
PSQL_PASSWORD=os.environ.get('PSQL_PASSWORD')
PSQL_URL=os.environ.get('PSQL_URL')

engine = create_engine(f"postgresql://{PSQL_USERNAME}:{PSQL_PASSWORD}@{PSQL_URL}")
Base.metadata.create_all(bind=engine)