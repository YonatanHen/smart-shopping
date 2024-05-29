import pandas as pd
import warnings

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from __future__ import division

#do not show warnings
warnings.filterwarnings("ignore")

def get_data():
    
    data = pd.read_csv('../../temp_data/Groceries_dataset.csv')
    data.columns = ['product_id', 'date', 'item_name']
    data.date = pd.to_datetime(data.date)
    data = data.sort_values(by='date')
    
    return data


def get_list():
    data = get_data()
    
    #Get last date when each item was purchased
    max_purchase_date = data.groupby(pd.Grouper(key='item_name')).date.max().reset_index(name='last_purchased')

    frequency_of_items = data.groupby(pd.Grouper(key='item_name')).size().reset_index(name='count')

    average_purchase_interval = data.groupby(pd.Grouper(key='item_name')).date.apply(lambda x: x.diff().mean()).reset_index(name='avg_interval')

    df = pd.merge(max_purchase_date,frequency_of_items,on='item_name')
    df = pd.merge(df, average_purchase_interval, on='item_name')

    df['last_purchased'] = pd.to_datetime(df['last_purchased'])
    df['avg_interval'] = pd.to_timedelta(df['avg_interval']).dt.total_seconds()
    df['last_purchased'] = pd.to_timedelta(df['avg_interval']).dt.total_seconds()

    df['count'].fillna(0, inplace=True)
    df['avg_interval'].fillna(0, inplace=True)

    print(df)

    X = df[['count', 'avg_interval', 'last_purchased']]  # Features
    y = df['item_name']  # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    print(X_train.shape)

    dtc = DecisionTreeClassifier()

    dtc.fit(X_train, y_train)

    y_pred = dtc.predict(X_test)
    print(y_pred, len(y_pred))

    # features = pd.DataFrame(dtc.feature_importances_, index= X.columns)



