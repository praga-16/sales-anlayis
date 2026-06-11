import pandas as pd

df = pd.read_csv("project_sales_data.csv")

print(df.shape)
print(df.head())
print(df['Status'].value_counts())