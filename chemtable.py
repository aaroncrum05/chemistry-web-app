import pandas as pd

#in pandas, the whole table is called a "Data Frame" hence the df listings
df = pd.read_csv("matchem.csv")

mc = df.dtypes

print(mc)


print(df.head(10))
