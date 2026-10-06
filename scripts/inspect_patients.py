import pandas as pd

'''Example of pandas Dataframe
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'age' : [23, 30, 18],
        'Country': ['USA', 'CANADA', 'UK']
}
df = pd.DataFrame(data) # by default it gives the index for the dataframe
print(df, type(df))
'''
file_path = "D:/Reshma Personal/Reshma Capstone Project/Healthcare-Data-Integration-Platform/data/raw/patients.csv"
df = pd.read_csv(file_path) #Load data from csv file

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))