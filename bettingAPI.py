import pandas as pd # use pandas to read the csv easily
import random
# charts.csv, all stream data comes from https://kworb.net/spotify/country/global_daily.html

def cleanStreams(streamStr):
    # convert the stream number to python readable integer
    return int(streamStr.replace('.','')) # just remove the period

def generateLines(streams): # generate the lines to bet on based off of the static current data.
    #May add trends in the future to make generation better.
    lines = [] # make a empty list to store the generated lines
    for stream in streams:
        # iterate over the streams
        base = cleanStreams(stream) # make a clean version of the stream num
        # add or subtract 1-3% to generate a random line
        adjustment = random.uniform(-0.03,0.03) # uniform rounds the number based off variance here
        line = int(base * (1+adjustment)) # cast to a int
        lines.append(line) # add the generationed line to the list
    return lines # return all the lines made

df = pd.read_csv("charts.csv") # read the csv and make the data frame hold it
df["Lines"] = generateLines(df["Streams"]) # take the stream data and generate lines
print(df)