import unittest
import sys
import os
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Product, List, Base
from DB.PsqlConnection import engine
from datetime import datetime

class LearnTest(unittest.TestCase):
    
    def test_func_1(self):
        pass
    
    def test_create_list(self):
        Base.metadata.create_all(bind=engine)

        new_list = List(date=datetime.now())

        # Define grocery items
        grocery_items = ["Eggs", "Chicken Breast", "Soy Milk"]

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

        session.add(new_list)

        session.commit()

        # Create product instances and associate them with the list
        for item in grocery_items:
            new_product = Product(item_name=item, list_id=new_list.id)
            session.add(new_product)

        # Commit the changes to the database
        session.commit()
        
if __name__ == '__main__':
    unittest.main()