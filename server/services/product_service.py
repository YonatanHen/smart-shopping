import pandas as pd
import warnings
import sys
import os
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB.PsqlConnection import engine
from models import Product


# do not show warnings
warnings.filterwarnings("ignore")


def get_all_products():
    Session = sessionmaker(bind=engine)

    session = Session()

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
