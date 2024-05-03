from typing import List
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship, column_property
from sqlalchemy.types import Date, DateTime
from data.DB.PsqlConnection import PSQLConnection

def main():
    
    engine = PSQLConnection()

    class Base(DeclarativeBase):
        pass

    class List(Base):
        __tablename__ = 'items_list'
        
        id: Mapped[int] = mapped_column(primary_key=True)
        date: Mapped[Date] = mapped_column(DateTime, nullable=False)
        
        __mapper_args__ = {
            "version_id_col": date,
            "version_id_generator": lambda v: datetime.now(),
        }

    class Item(Base):
        __tablename__ = 'item'
        
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(50))
    

if __name__ == '__main__':
    main()