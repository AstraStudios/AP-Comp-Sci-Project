import requests

url = "https://realpython.github.io/fake-jobs/"
pageData = requests.get(url)

print(pageData.text)