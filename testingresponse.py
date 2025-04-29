import requests

url = "https://charts.spotify.com/charts/view/regional-global-daily/latest"
pageData = requests.get(url)

print(pageData.text)