import requests # request stuff from internet
from bs4 import BeautifulSoup # find stuff on html pages https://beautiful-soup-4.readthedocs.io/en/latest/
import pandas as pd # manipulate data https://pandas.pydata.org/
import json # save stuff

print("Loading...")

# fetch from kworb.net stream data https://kworb.net/spotify/country/us_daily.html
spotifyStreamURL = "https://kworb.net/spotify/country/us_daily.html"

def fetchSpotifyCharts():
    response = requests.get(spotifyStreamURL)

    if response.status_code != 200:
        print("Failed to get charts")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    scriptTag = soup.find("script",{"id":"daily"})
    
    if not scriptTag:
        print("Failed to find data on charts")
        return
    
    # attempt to convert it to a json file
    data = scriptTag.string
    chartsData = eval(data) # make the string a dictionary
    
    # extract the song data
    try:
        chartEntries = chartsData["props"]["pageProps"]["chartEntries"]
        chartList = []

        for entry in chartEntries:
            rank = entry["chartEntryData"]["currentRank"]
            songName = entry["trackMetadata"]["trackName"]
            streams = entry["chartEntryData"].get("streams","N/A")

            chartList.append({"rank":rank,"song":songName,"streams":streams})
        # convert to a data frame
        df = pd.DataFrame(chartList, columns=["rank","song","streams"])
        print(df)
    except KeyError:
        print("Faled to parse the charts data")

fetchSpotifyCharts()