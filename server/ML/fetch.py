import csv
import pandas as pd

data = pd.read_csv('data/Groceries_dataset.csv')
data.columns = ['memberID', 'Date', 'itemName']
data.Date = pd.to_datetime(data.Date)
data.memberID = data['memberID'].astype('str')

print(data)

Frequency_of_items = data.groupby(pd.Grouper(key='itemName')).size().reset_index(name='count')
print(Frequency_of_items)
    
    
        
