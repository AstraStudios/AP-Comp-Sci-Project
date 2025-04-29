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
    response = requests.get(spotifyStreamURL)

    if response.status_code != 200:
        print("Failed to get charts")
        return
    
    # use beautiful soup to read info from the page
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
        with open("streams.json",'w') as f:
            json.dump(chartList,f)
        print(df)
    except KeyError:
        print("Faled to parse the charts data")

fetchSpotifyCharts()