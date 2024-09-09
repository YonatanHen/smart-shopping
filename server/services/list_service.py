import pandas as pd
import warnings
import sys
import os
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Product, List, Base
from .utils.create_db_session import get_session
from .utils.errors.sqlalchemy_error import handle_sqlalchemy_error
from sqlalchemy.orm import sessionmaker
from DB.PsqlConnection import engine
#Do not show warnings
warnings.filterwarnings("ignore")

def get_lists(session=None):
    try:
        if session is None:
            session = get_session()
            
        res = session.query(List).all()
        list_data = pd.DataFrame([{
            'list_id': item.id,
            'date': item.date
        } for item in res])
        return list_data
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
    except Exception as e:
        raise Exception("An unexpected error occurred") from e
    finally:
        if os.getenv("ENV")=="Production":
            session.close()

def add_list(groceries_items, session=None):
    try:
        if session is None:
            session = get_session()
            
        new_list = List(date=datetime.now())
        session.add(new_list)
        session.commit()

        for item in groceries_items:
            new_product = Product(item_name=item, list_id=new_list.id)
            session.add(new_product)
        
        session.commit()
        return new_list
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
    except Exception as e:
        raise Exception("An unexpected error occurred") from e
    finally:
        if os.getenv("ENV")=="Production":
            session.close()

def add_products_to_list(list_id, products_list, session=None):    
    try:
        if session is None:
            session = get_session()
    
        # Fetch the list from the DB
        list_to_update = session.query(List).filter(List.id == list_id).first()
        
        if list_to_update is None:
            raise ValueError(f"List with id {list_id} does not exist.")
        
        # Add item/s to an existing list
        new_products = set(products_list)
        print(list_to_update.products)
        for product in new_products:
            if product not in list_to_update.products:
                new_product = Product(item_name=product, list_id=list_to_update.id)
                session.add(new_product)
        
        session.commit()
        
        updated_list=session.query(List).filter(List.id == list_id).first()
        list_data = {
            "id": updated_list.id,
            "date": updated_list.date.isoformat(),
            "products": [p.item_name for p in updated_list.products]
        }
        return list_data
        
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
    except ValueError as e:
        raise
    except Exception as e:
        raise Exception("An unexpected error occurred") from e
    finally:
        if os.getenv("ENV")=="Production":
            session.close()          
            
def delete_list(list_id, session=None):
    try:
        if session is None:
            session = get_session()
            
        list_to_delete = session.query(List).filter(List.id == list_id).first()
        if not list_to_delete:
            raise ValueError(f"List #{list_id} doesn't exist.")
        
        deleted_list = {
            'id': list_to_delete.id,
            'date': list_to_delete.date,
        }
        
        products_to_delete = session.query(Product).filter(list_id == Product.list_id).all()
        
        for p in products_to_delete:
            session.delete(p)
        
        session.delete(list_to_delete)    
        
        session.commit()
        
    except SQLAlchemyError as e:
            raise ValueError("Error deleting list.") from e
    except Exception as e:
        raise Exception("An unexpected error occurred") from e
    finally:
        if os.getenv("ENV")=="Production":
            session.close()
        
        return deleted_list