from sqlalchemy.orm import sessionmaker, scoped_session
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.product_service import *
from services.list_service import *
from models import List, Base
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
        
    def test_01_create_list(self):
        """
        This function tests the creation of a list with some products.
        """
        # Define grocery items
        grocery_items = ["Eggs", "Chicken Breast", "Soy Milk"]

        new_list=add_list(grocery_items, self.session)
        
        # Assertions to ensure the list and products were created
        created_list = self.session.query(List).filter_by(id=new_list.id).one()
        self.assertIsNotNone(created_list)
        self.assertEqual(created_list.products.count(), len(grocery_items))
        for product in created_list.products:
            self.assertIn(product.item_name, grocery_items)
            
    def test_02_update_product_in_list(self):
        """
        This function test an addition of products of an existing list.
        """
        new_grocery_items = ["Bread", "Sugar"]
        
        list_to_update = self.session.query(List).first()
                
        updated_list = add_products_to_list(list_to_update.id, new_grocery_items,self.session)
        
        list_after_update = self.session.query(List).filter_by(id=updated_list.id).one()
        
        list_items_after_update = [p.item_name for p in list_after_update.products]
        
        print(f"list after update id is {list_after_update.id}, list products are: {list_items_after_update}")
        
        self.assertIsNotNone(list_after_update)
        self.assertEqual(list_after_update.products.count(), len(list_items_after_update))
        for product in new_grocery_items:
            self.assertIn(product, list_items_after_update)

    def test_03_create_empty_list(self):
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