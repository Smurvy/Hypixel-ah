import requests

# There is a lot of junk in the initial json that I dont need - mostly special characters from ingame that are just printed as "§" along
# with a few extra statements that I don't want in there
def getJson():
    r = requests.get("https://api.hypixel.net/skyblock/auctions")
    return r.json()

