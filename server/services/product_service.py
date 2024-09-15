import pandas as pd
import warnings
import sys
import os
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Product
from .utils.errors.sqlalchemy_error import handle_sqlalchemy_error
from .utils.create_db_session import get_session
from DB.PsqlConnection import engine

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

        products_data = pd.DataFrame([{
            'item_name': item.item_name,
            'amount': item.amount
        } for item in res])

    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
    except Exception as e:
        raise Exception("An unexpected error occurred") from e
    finally:
        if os.getenv("ENV") == "Production":
            session.close()

        return products_data


def delete_product(product_name, list_id, session=None):
    try:
        if session is None:
            session = get_session()

        product_to_delete = session.query(Product).filter(
            and_(
                list_id == Product.list_id,
                func.lower(product_name) == func.lower(Product.item_name)
            )
        ).first()

        if product_to_delete is None:
            return None

        session.delete(product_to_delete)
        session.commit()
        
        updated_list = get_products_by_list_id(list_id, session)
        return updated_list
    
    except ValueError as e:
        raise
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)
    except Exception as e:
        raise Exception("An unexpected error occurred") from e

    finally:
        if os.getenv("ENV") == "Production":
            session.close()

        
