import csv

with open('data/Groceries_dataset.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)