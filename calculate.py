import pandas as pd


df = pd.read_csv("output.csv")

total_tech = 0

for count in df['count']:
    total_tech = total_tech + int(count)



print(f"Total Technologies Found --- > {total_tech}/477")

