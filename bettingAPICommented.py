import pandas as pd # use pandas to read the csv easily
import random
# charts.csv, all stream data comes from https://kworb.net/spotify/country/global_daily.html
# code written by Luke Brittain unless otherwise stated

def cleanStreams(streamStr):
    # convert the stream number to python readable integer
    return int(streamStr.replace('.','')) # just remove the period

def formatNumber(num): # user QOL thing to make it more readable
    number = int(num)
    return "{:,}".format(number) # using format -> https://www.w3schools.com/python/ref_string_format.asp

def generateLines(streams): # generate the lines to bet on based off of the static current data.
    #May add trends in the future to make generation better.
    lines = [] # make a empty list to store the generated lines
    for stream in streams:
        # iterate over the streams
        base = cleanStreams(stream) # make a clean version of the stream num
        # add or subtract 1-3% to generate a random line
        adjustment = random.uniform(-0.03,0.03) # uniform rounds the number based off variance -> https://www.w3schools.com/python/ref_random_uniform.asp
        line = int(base * (1+adjustment)) # cast to a int
        lines.append(line) # add the generated line to the list
    return lines # return all the lines made

def placeBet(df):
    # show the top 10 songs and let the user pick
    print("\n Top 10 Songs Today:")
    print(df[["Rank", "Song", "Artist", "Lines"]].head(10).to_string(index=False))

    try: # choosing a song by rank
        rank = int(input("\nSelect a song by rank: "))
        selected = df[df["Rank"]==rank].iloc[0] # iloc selects a row in a dataframe -> https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html

        print(f"\nYou selected {selected['Song']} by {selected['Artist']}") # print to make sure the user knows
        print(f"Line is: {selected['Lines']:,} streams")

        # place the actual bet
        bet = input("OVER or UNDER? ").strip().lower() # make sure its lower case
        if bet not in ["over", "under"]:
            print("Invalid bet choice") # essientially throw an error
            return # go back
        
        # store or print the bet, right now just printing
        print(f"\nBet places: {bet.upper()} on {selected['Song']} at line {selected['Lines']:,} streams")

        # in the future extend this to record to a file or a database
        return {
            "song": selected['Song'], # make sure the song is known
            "artist": selected['Artist'],
            "line": selected['Lines'], # save the line the bet was taken at
            "choice": bet # save this to check in simulation
        }
    
    except Exception as e:
        print("Error placing bet:", e) # just in case theres an error

def simulateBet(bet): # a very simple random simulation
    actualStreams = int(bet['line'] * random.uniform(0.95,1.05)) # +- 5% of line uniform -> https://www.w3schools.com/python/ref_random_uniform.asp
    outcome = 'over' if actualStreams > bet['line'] else 'under'
    win = bet['choice'] == outcome # check if the stored choice is equal to the outcome

    cleanActualStreams = formatNumber(actualStreams)

    print("Simulating your bet...") # just some theatrics
    print(f"Actual streams: {cleanActualStreams}")
    print(f"You bet {bet['choice'].upper()} {bet['line']:,}")
    print("You WON!" if win else "You LOST!")

    return {
        "actualstreams": actualStreams, # keep it straight int for computer reading
        "won": win
    }

df = pd.read_csv("charts.csv") # read the csv and make the data frame hold it
df["Lines"] = generateLines(df["Streams"]) # take the stream data and generate lines
bet = placeBet(df) # place the bet as a variable so that we can use it to simulate
simulateBet(bet) # finish by simulating!