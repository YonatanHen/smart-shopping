from __future__ import division
#import libraries
from datetime import datetime, timedelta,date
import pandas as pd
from sklearn.metrics import classification_report,confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans

#do not show warnings
import warnings
warnings.filterwarnings("ignore")

#import plotly for visualization
# import plotly.plotly as py
# import plotly.offline as pyoff
# import plotly.graph_objs as go

#import machine learning related libraries
from sklearn.svm import SVC
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from sklearn.model_selection import KFold, cross_val_score, train_test_split


data = pd.read_csv('data/Groceries_dataset.csv')
data.columns = ['product_id', 'date', 'item_name']
data.date = pd.to_datetime(data.date)
data.memberID = data['product_id'].astype('str')
data = data.sort_values(by='date')

#Get last date when each item was purchased
max_purchase_date = data.groupby(pd.Grouper(key='item_name')).date.max().reset_index(name='last_purchased')

frequency_of_items = data.groupby(pd.Grouper(key='item_name')).size().reset_index(name='count')

average_purchase_interval = data.groupby('item_name').date.apply(lambda x: x.diff().mean()).reset_index(name='avg_interval')

# TODO: https://towardsdatascience.com/predicting-next-purchase-day-15fae5548027#:~:text=For%20RFM%2C%20to%20not%20repeat%20Part%202%2C%20we%20share%20the%20code%20block%20and%20move%20forward%3A 



