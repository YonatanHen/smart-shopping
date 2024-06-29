import pandas as pd
import warnings
import sys
import os
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Product, List, Base

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB.PsqlConnection import engine
from models import Product

#do not show warnings
warnings.filterwarnings("ignore")

def get_products():
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    res = session.query(Product).all()
    
    products_data = pd.DataFrame([{
        'product_id': item.id,
        'list': item.list_id,
        'item_name': item.item_name
    } for item in res])
    
    # Close the session
    session.close()
    
    return products_data

def add_products(groceries_items, session=None):
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