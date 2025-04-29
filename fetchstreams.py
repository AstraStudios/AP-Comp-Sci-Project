import requests # request stuff from internet
import pandas as pd # manipulate data https://pandas.pydata.org/
import json # save stuff

def fetchSpotifyCharts():
    # fetch from the official spotify website https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-daily-latest
    spotifyStreamURL = "https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-daily-latest"


    headers = {
        "Accept":"application/json",
        "App-Platform":"Web",
        "Authorization":"", # currently works without auth
    }
    response = requests.get(spotifyStreamURL, headers=headers)

    if response.status_code != 200:
        print("Failed to get charts")
        return
    
    data = response.json()

    chartList = [] # make a empty list to store the chart
    for entry in data["entries"]["items"]:
        rank = entry["chartEntryData"]["currentRank"] # find the current rank of the song
        songName = entry["trackMetadata"]["trackName"] # get the name
        streams = entry["chartEntryData"].get("streams", "N/A")

        chartList.append([rank,songName,streams]) # add all the data to the list
    
    # use a dataframe to show
    df = pd.DataFrame(chartList, columns=["Rank", "Song", "Streams"])
    print(df)

# run
fetchSpotifyCharts()