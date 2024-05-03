from sqlalchemy import create_engine
import os

def PSQLConnection():
    PSQL_USERNAME=os.environ.get('PSQL_USERNAME')
    PSQL_PASSWORD=os.environ.get('PSQL_PASSWORD')
    PSQL_URL=os.environ.get('PSQL_URL')

    engine = create_engine(f"postgresql://{PSQL_USERNAME}:{PSQL_PASSWORD}@{PSQL_URL}/postgres")

    try:
        with engine.connect() as connection_str:
            print('Successfully connected to the PostgreSQL database')
        return engine
    except Exception as e:
        print(f'Failed to connect: {e}')
    
