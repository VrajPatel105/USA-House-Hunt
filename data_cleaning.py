import pandas as pd
import numpy as np
df = pd.read_csv('housing-data.csv')

# dropping the nan values in the below cols. Note that the below cols didnt have 10% of the nan values, so can be removed based on the data set size of 2.2M
df.dropna(subset=['price','street','city','state','zip_code','brokered_by'], inplace=True)

df.drop_duplicates()

df.rename(columns={'brokered_by':'Property ID', 'house_size':'house_size_sq_ft','price':'price (USD)'}, inplace=True)

df.drop(columns=['street'], inplace=True)

df['prev_sold_date'] = df['prev_sold_date'].fillna('Undisclosed')

df['house_size_sq_ft'] = df['house_size_sq_ft'].fillna(df['house_size_sq_ft'].median())


df['price (USD)'] = df['price (USD)'].replace({'\$': '', ',': ''}, regex=True).astype('float')

df['bed'] = df['bed'].fillna(df['bed'].median())
df['bath'] = df['bath'].fillna(df['bath'].median())
df['acre_lot'] = df['acre_lot'].fillna(df['acre_lot'].median())

temp = ['bed','bath','zip_code','Property ID']
for i in temp:
  df[i] = df[i].astype('int')

df['status'] = df['status'].replace('for_sale', 'For Sale')
df['status'] = df['status'].replace('ready_to_build', 'Ready to build')
df['status'] = df['status'].replace('sold','Sold')

df['price (USD)'] = df['price (USD)'].apply(lambda x: f'{x:,.2f}')

# Remove any non-date strings first
df['prev_sold_date'] = df['prev_sold_date'].replace(['nan', 'NaN', 'undisclosed', 'Undisclosed'], np.nan)
# Then convert to datetime
df['prev_sold_date'] = pd.to_datetime(df['prev_sold_date'], errors='coerce')


df.to_csv('cleaned_housing_data.csv', index=False)