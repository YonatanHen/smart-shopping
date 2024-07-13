import pandas as pd
import warnings
import sys
import os
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Product, List, Base

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import List

from DB.PsqlConnection import engine

#do not show warnings
warnings.filterwarnings("ignore")

def get_lists():
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    res = session.query(List).all()
    
    list_data = pd.DataFrame([{
        'list_id': item.id,
        'date': item.date
    } for item in res])
    
    # Close the session
    session.close()
    
    return list_data

def add_list(groceries_items, session=None):
    Base.metadata.create_all(bind=engine)

    new_list = List(date=datetime.now())

    if session is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

    session.add(new_list)

    session.commit()

    # Create product instances and associate them with the list
    for item in groceries_items:
        new_product = Product(item_name=item, list_id=new_list.id)
        session.add(new_product)

    # Commit the changes to the database
    session.commit()

    return new_list

def edit_list(products_data, session=None):
    Base.metadata.create_all(bind=engine)
    
    if session is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
    
    # Get the list from the DB
    
    # Edit the list accordingly + change date
    
    # 


