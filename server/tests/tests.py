from sqlalchemy.orm import sessionmaker, scoped_session
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.product_service import *
from services.list_service import *
from services.utils.calculate_list import *
from models import List, Base
from DB.PsqlConnection import engine
from datetime import datetime

class ListTest(unittest.TestCase):
    
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
        grocery_items = {"Eggs": 2, "Chicken Breast": 1, "Soy Milk": 4}

        new_list=add_list(grocery_items, self.session)
        
        # Assertions to ensure the list and products were created
        created_list = self.session.query(List).filter_by(id=new_list.id).one()
        self.assertIsNotNone(created_list)
        self.assertEqual(created_list.products.count(), len(grocery_items))
        for product in created_list.products:
            self.assertIn(product.item_name, grocery_items)
            
            
    def test_02_add_products_to_list(self):
        """
        This function test an addition of products of an existing list.
        """
        new_grocery_items = {"Bread": 2, "Sugar": 1}
        
        list_to_update = self.session.query(List).first()
                
        updated_list = add_products_to_list(list_to_update.id, new_grocery_items,self.session)
        list_id = updated_list['id']
        list_after_update = self.session.query(List).filter_by(id=list_id).one()
        
        list_items_after_update = {p.item_name: p.amount for p in list_after_update.products}
        
        print(f"Test #2: list after update id is {list_after_update.id}, list products are: {list_items_after_update}\n")
        
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
    
    
    def test_04_delete_list(self):
        """
        This function tests the deletion of a list.
        """
        grocery_items = {"Eggs": 1, "Chicken Breast": 1, "Soy Milk": 1}

        new_list=add_list(grocery_items, self.session)
        
        get_created_list = self.session.query(List).filter_by(id=new_list.id).all()
        
        self.assertNotEqual(get_created_list,[])
        
        get_deleted_list = delete_list(new_list.id,self.session)

        # Check whether the deleted list has some content
        self.assertNotEqual(get_deleted_list, [])
        
        # Check whether the list deleted
        self.assertEqual(self.session.query(List).filter_by(id=new_list.id).all(), [])
        
        
    def test_05_delete_product(self):
        """
        This function tests the deletion of a product from a list.
        """
        grocery_items = {"Eggs": 1, "Chicken Breast": 4, "Soy Milk": 6}
        
        new_list=add_list(grocery_items, self.session)
        
        deleted_product = delete_product("Eggs", new_list.id, self.session)
                    
        self.assertIsNotNone(deleted_product)    
        
        list_after_delete = get_products_by_list_id(new_list.id, self.session)
        
        list_records = list_after_delete.to_dict(orient="records")
        
        # Extract item names from the list of dictionaries
        products_after_delete = {p['item_name'] for p in list_records}

        self.assertNotIn("Eggs", products_after_delete)
        
        self.assertIn("Chicken Breast", products_after_delete)
        
        delete_product_2 = delete_product("Eggs", new_list.id, self.session)
        
        #Check whether the function returns None (as expected) if the product does not exist
        self.assertIsNone(delete_product_2)
        
        
    def test_06_create_list_with_duplicated_products(self):
        """
        This function tests the creation of a list with duplicated products.
        According to limitations in Python, dictionary with duplicated keys will not be processed and only the last key will be kept.
        """
        # Define grocery items
        grocery_items = {"Eggs": 2, "Eggs": 1, "Soy Milk": 4}

        new_list=add_list(grocery_items, self.session)
        
        # Assertions to ensure the list and products were created
        created_list = self.session.query(List).filter_by(id=new_list.id).one()
        
        print(f"Test #6: Created list: {{p.item_name: p.amount for p in created_list.products}}\n")
        
        self.assertIsNotNone(created_list)
        self.assertEqual(created_list.products.count(), len(grocery_items))
        for product in created_list.products:
            self.assertIn(product.item_name, grocery_items)
            
            
    def test_07_suggest_list(self):
        """
        This function tests the suggestion of a list based on the user's shopping history. 
        """
        add_list({"Eggs": 1, "Chicken Breast": 4, "Soy Milk": 6, "Sugar": 1, "Salt": 1, "Apples": 10}, self.session)
        add_list({"Milk": 2, "Eggs": 1, "Bread": 1, "Chicken Breast": 2}, self.session)
        
        suggested_list_1 = calculate_new_list()
        suggested_list_2 = calculate_new_list(0.4)
        
        print(f"Test #7: Suggested list 1: {suggested_list_1}\n")
        print(f"Test #7: Suggested list 2: {suggested_list_2}\n")
        
        self.assertIsNotNone(suggested_list_1)
        self.assertIsNotNone(suggested_list_2)
        self.assertNotEqual(str(suggested_list_1), str(suggested_list_2))
        
        
    def test_08_update_product(self):
        """
        This function tests the update of a product in a list
        """
        grocery_items = {"Eggs": 2, "Bread": 1, "Soy Milk": 4}

        new_list = add_list(grocery_items, self.session)
        
        new_product_data = {"item_name": "Eggplant", "amount": 1}
         
        updated_product = update_product("Eggs", new_list.id, new_product_data ,self.session)
        
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product.item_name, "Eggplant")
        self.assertEqual(updated_product.amount, 1)
        
if __name__ == '__main__':
    unittest.main()