from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    amount = Column(Integer, default=1)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class List(Base):
    __tablename__ = "lists"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)

    # Relationship to Product
    products = relationship('Product', backref='list', lazy='dynamic')

