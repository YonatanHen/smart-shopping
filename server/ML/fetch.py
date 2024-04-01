from __future__ import division
#import libraries
import pandas as pd
from typing import Dict, Text

import numpy as np
import tensorflow as tf

import tensorflow_datasets as tfds
import tensorflow_recommenders as tfrs
#do not show warnings
import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('data/Groceries_dataset.csv')
data.columns = ['product_id', 'date', 'item_name']
data.date = pd.to_datetime(data.date)
data = data.sort_values(by='date')

#Get last date when each item was purchased
max_purchase_date = data.groupby(pd.Grouper(key='item_name')).date.max().reset_index(name='last_purchased')

frequency_of_items = data.groupby(pd.Grouper(key='item_name')).size().reset_index(name='count')

average_purchase_interval = data.groupby('item_name').date.apply(lambda x: x.diff().mean()).reset_index(name='avg_interval')


# TODO: https://towardsdatascience.com/predicting-next-purchase-day-15fae5548027#:~:text=For%20RFM%2C%20to%20not%20repeat%20Part%202%2C%20we%20share%20the%20code%20block%20and%20move%20forward%3A 



