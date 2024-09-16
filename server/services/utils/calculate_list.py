import pandas as pd
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..product_service import get_all_products
from ..list_service import get_lists


def calculate_new_list(test_set=0.3):
    products_data = get_all_products()
    lists_data = get_lists()
    
    if len(products_data) == 0 or len(lists_data)==0:
        return None
    
    data = pd.merge(products_data, lists_data, left_on='list', right_on='list_id')
    
    #Get last date when each item was purchased
    max_purchase_date = data.groupby(pd.Grouper(key='item_name')).date.max().reset_index(name='last_purchased')

    #Calculate the sum of amounts for each item
    total_amount = data.groupby('item_name')['amount'].sum().reset_index(name='total_amount')
    
    #Calculate the average amount for each item
    average_amount = data.groupby('item_name')['amount'].mean().reset_index(name='avg_amount')

    average_purchase_interval = data.groupby(pd.Grouper(key='item_name')).date.apply(lambda x: x.diff().mean()).reset_index(name='avg_interval')

    df = pd.merge(max_purchase_date,total_amount,on='item_name')
    df = pd.merge(df, average_amount, on='item_name')
    df = pd.merge(df, average_purchase_interval, on='item_name')

    df['total_amount'] = df['total_amount'].fillna(0)
    df['avg_amount'] = df['avg_amount'].fillna(0)
    df['avg_interval'] = df['avg_interval'].fillna(pd.Timedelta(seconds=0))

    # Convert 'last_purchased' to seconds since Unix epoch for numerical representation
    df['last_purchased'] = pd.to_datetime(df['last_purchased'])
    df['last_purchased'] = (df['last_purchased'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    
    df['avg_interval'] = pd.to_timedelta(df['avg_interval']).dt.total_seconds()

    X = df[['total_amount', 'avg_interval', 'avg_amount', 'last_purchased']]  # Features
    y = df['item_name']  # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_set, random_state=42)

    dtc = DecisionTreeClassifier()

    dtc.fit(X_train, y_train)
    y_pred = dtc.predict(X_test)
    
    res = []
    for index, row in df.iterrows():
        if row['item_name'] in y_pred:
            res.append({
                'item_name': row['item_name'],
                'amount': round(row['avg_amount'])
            })

    return res