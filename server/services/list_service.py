import pandas as pd
import warnings
import sys
import os
from sqlalchemy.orm import sessionmaker

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB.PsqlConnection import psql_connection
from product_service import get_products
from models import List

#do not show warnings
warnings.filterwarnings("ignore")

def get_lists():
    engine=psql_connection()
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    res = session.query(List).all()
    
    list_data = pd.DataFrame([{
        'list_id': item.id,
        'date': item.date
    } for item in res])
    
    # Close the session
    session.close()
    
    return list_data

def create_new_list():
    products_data = get_products()
    lists_data = get_lists()
    
    data = pd.merge(products_data, lists_data, left_on='list', right_on='list_id')
    
    #Get last date when each item was purchased
    max_purchase_date = data.groupby(pd.Grouper(key='item_name')).date.max().reset_index(name='last_purchased')

    frequency_of_items = data.groupby(pd.Grouper(key='item_name')).size().reset_index(name='count')

    average_purchase_interval = data.groupby(pd.Grouper(key='item_name')).date.apply(lambda x: x.diff().mean()).reset_index(name='avg_interval')

    df = pd.merge(max_purchase_date,frequency_of_items,on='item_name')
    df = pd.merge(df, average_purchase_interval, on='item_name')

    df['count'].fillna(0, inplace=True)
    df['avg_interval'].fillna(pd.Timedelta(seconds=0), inplace=True)
    
    df['last_purchased'] = pd.to_datetime(df['last_purchased'])
    df['avg_interval'] = pd.to_timedelta(df['avg_interval']).dt.total_seconds()
    df['last_purchased'] = pd.to_timedelta(df['avg_interval']).dt.total_seconds()

    df['count'].fillna(0, inplace=True)
    df['avg_interval'].fillna(0, inplace=True)

    print(df)

    X = df[['count', 'avg_interval', 'last_purchased']]  # Features
    y = df['item_name']  # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    dtc = DecisionTreeClassifier()

    dtc.fit(X_train, y_train)

    y_pred = dtc.predict(X_test)
    print(y_pred, len(y_pred))


