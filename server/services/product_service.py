import pandas as pd
import warnings
import sys
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB.PsqlConnection import engine
from .utils.create_db_session import get_session
from models import Product


# do not show warnings
warnings.filterwarnings("ignore")


def get_all_products():
    session = get_session()

    res = session.query(Product).all()

    products_data = pd.DataFrame([{
        'product_id': item.id,
        'list': item.list_id,
        'item_name': item.item_name,
        'amount': item.amount
    } for item in res])

    # Close the session
    session.close()

    return products_data

def get_products_by_list_id(list_id, session=None):
    try:
        if session is None:
            session = get_session()
                        
        res = session.query(Product).filter_by(list_id=list_id).all()
        print(res)
        
        products_data = pd.DataFrame([{
            'item_name': item.item_name,
            'amount': item.amount
        } for item in res])
        
        return products_data
    
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
    except Exception as e:
        raise Exception("An unexpected error occurred") from e
    finally:
        if os.getenv("ENV")=="Production":
            session.close()

def delete_product(product_name, list_id, session=None):
    try:
        if session is None:
            session = get_session()
        
        product = session.query(Product).filter_by(item_name=product_name, list_id=list_id).first()
        if not product:
            raise ValueError(f"No product found with name '{product_name}' and list_id '{list_id}' found.")
        
        product_to_delete = session.query(Product).filter(list_id == Product.list_id and product_name == Product.item_name).first()
        session.delete(product_to_delete)
        
        session.commit()
        
        updated_list = session.query
    except ValueError as e:
        raise
    except Exception as e:  
        raise Exception("An unexpected error occurred") from e     
    
    finally:
        
        if os.getenv("ENV")=="Production":
            session.close()
        
        return 
        