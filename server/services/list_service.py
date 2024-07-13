import pandas as pd
import warnings
import sys
import os
from sqlalchemy.orm import sessionmaker
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB.PsqlConnection import engine
from models import Product, List, Base

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

def add_products_to_list(list_id, products_list, session=None):
    Base.metadata.create_all(bind=engine)
    
    if session is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
    
    # Fetch the list from the DB
    list_to_update = session.query(List).filter(List.id == list_id).first()
    print(list_to_update.id)
    
    if list_to_update is None:
        raise ValueError(f"List with id {list_id} does not exist.")
    
    # Add item/s to an existing list
    new_products = set(products_list)
    
    for product in new_products:
        if product not in list_to_update.products:
            new_product = Product(item_name=product, list_id=list_to_update.id)
            session.add(new_product)
    
    session.commit()
    
    return list_to_update
            


