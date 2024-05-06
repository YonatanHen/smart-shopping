from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from DB.PsqlConnection import Base,engine
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    

class List(Base):
    __tablename__ = "lists"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)

Base.metadata.create_all(bind=engine)

new_list = List(date=datetime.now())

# Define grocery items
grocery_items = ["Apples", "Bananas", "Milk", "Bread", "Eggs"]

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

session.add(new_list)

session.commit()

# Create product instances and associate them with the list
for item in grocery_items:
    new_product = Product(name=item, list_id=new_list.id)
    session.add(new_product)

# Commit the changes to the database
session.commit()