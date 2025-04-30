import pandas as pd # use pandas to read the csv easily
import random
# charts.csv, all stream data comes from https://kworb.net/spotify/country/global_daily.html
# code written by Luke Brittain unless otherwise stated

def cleanStreams(streamStr):
    return int(streamStr.replace('.',''))

def formatNumber(num):
    number = int(num)
    return "{:,}".format(number) # helpful reference -> https://www.reddit.com/r/learnpython/comments/t5japj/is_format_still_efficient_and_used/

def generateLines(streams):
    lines = []
    for stream in streams:
        base = cleanStreams(stream)
        adjustment = random.uniform(-0.03,0.03)
        line = int(base * (1+adjustment))
        lines.append(line)
    return lines

def placeBet(df):
    print("\n Top 10 Songs Today:")
    print(df[["Rank", "Song", "Artist", "Lines"]].head(10).to_string(index=False))

    try:
        rank = int(input("\nSelect a song by rank: "))
        selected = df[df["Rank"]==rank].iloc[0]

        print(f"\nYou selected {selected['Song']} by {selected['Artist']}")
        print(f"Line is: {selected['Lines']:,} streams")

        bet = input("OVER or UNDER? ").strip().lower()
        if bet not in ["over", "under"]:
            print("Invalid bet choice")
            return
        
        print(f"\nBet places: {bet.upper()} on {selected['Song']} at line {selected['Lines']:,} streams")

        return {
            "song": selected['Song'],
            "artist": selected['Artist'],
            "line": selected['Lines'],
            "choice": bet
        }
    
    except Exception as e:
        print("Error placing bet:", e)

def simulateBet(bet):
    actualStreams = int(bet['line'] * random.uniform(0.95,1.05))
    outcome = 'over' if actualStreams > bet['line'] else 'under'
    win = bet['choice'] == outcome

    cleanActualStreams = formatNumber(actualStreams)

    print("Simulating your bet...")
    print(f"Actual streams: {cleanActualStreams}")
    print(f"You bet {bet['choice'].upper()} {bet['line']:,}")
    print("You WON!" if win else "You LOST!")

    return {
        "actualstreams": actualStreams,
        "won": win
    }

df = pd.read_csv("charts.csv")
df["Lines"] = generateLines(df["Streams"])
bet = placeBet(df) 
simulateBet(bet) 