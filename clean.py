import pandas as pd

df = pd.read_csv('data.csv')

# Getting rid of the quotation marks and the empty spaces
df['root_domain'] = df['root_domain'].str.strip().str.strip('"')
df = df.drop_duplicates()

# Saving the data in a clean csv
df.to_csv('clean_data.csv', index=False)







