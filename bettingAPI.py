import pandas as pd # use pandas to read the csv easily
# as stated on charts.csv, all stream data comes from https://kworb.net/spotify/country/global_daily.html

df = pd.read_csv("charts.csv") # read the csv and make the data frame hold it

print(df)