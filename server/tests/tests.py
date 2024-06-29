from sqlalchemy.orm import sessionmaker, scoped_session
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.product_service import *
from models import Product, List, Base
from DB.PsqlConnection import engine
from datetime import datetime

class LearnTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        This method creates a new DB session.
        """
        Base.metadata.create_all(bind=engine)
        cls.Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    
    @classmethod
    def tearDownClass(cls):
        """
        This method drops thw whole data we have inserted into the DB for testing purposes.
        """
        Base.metadata.drop_all(bind=engine)
        cls.Session.remove()
        
    def setUp(self):
        """
        Method called to prepare the DB session for test fixture.
        """
        self.session = self.Session()
        
    def tearDown(self):
        """
        Method invoked immediately after the test method has been called and the results recorded.
        The method closes the session and rolls back to the changes recorded as part of the testing fixture.
        """
        self.session.rollback()
        self.session.close()
        
    def test_create_list(self):
        """
        This function tests the creation of a list with some products.
        """
        # Define grocery items
        grocery_items = ["Eggs", "Chicken Breast", "Soy Milk"]

        new_list=add_products(grocery_items, self.session)
        
        # Assertions to ensure the list and products were created
        created_list = self.session.query(List).filter_by(id=new_list.id).one()
        self.assertIsNotNone(created_list)
        self.assertEqual(created_list.products.count(), len(grocery_items))
        for product in created_list.products:
            self.assertIn(product.item_name, grocery_items)
            
    def test_create_empty_list(self):
        """
        This function tests the creation of an empty list.
        """
        new_list = List(date=datetime.now())

        self.session.add(new_list)
        self.session.commit()
        
        # Assertions to ensure the empty list was created
        created_list = self.session.query(List).filter_by(id=new_list.id).one()
        self.assertIsNotNone(created_list)
        self.assertEqual(created_list.products.count(), 0)
    
if __name__ == '__main__':
    unittest.main()