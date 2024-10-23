import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models import Base

load_dotenv()

PSQL_USERNAME=os.getenv('PSQL_USERNAME')
PSQL_PASSWORD=os.getenv('PSQL_PASSWORD')
PSQL_URL=os.getenv('PSQL_URL')

engine = create_engine(f"postgresql://{PSQL_USERNAME}:{PSQL_PASSWORD}@{PSQL_URL}")
Base.metadata.create_all(bind=engine)