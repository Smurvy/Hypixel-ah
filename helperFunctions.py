import requests
import sqlite3

def getJson(pageNum):
    r = requests.get(f"https://api.hypixel.net/skyblock/auctions?page={pageNum}")
    return r.json()

def convertFromUUIDtoUsername(uuid):
    data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
    print(data["name"])

def checkIfTableExists(cur):
    # check if the table exists
    try:
        cur.execute("SELECT * FROM currentAuctions")
        return True

    except sqlite3.OperationalError:
        cur.execute("""
                        CREATE TABLE currentAuctions (
                            itemName TEXT,
                            itemTier TEXT,
                            startDate TEXT,
                            endDate TEXT,
                            itemCategory TEXT,
                            itemPrice INTEGER,
                            isBin TEXT,
                            highestBid INTEGER,
                            auctioneer TEXT);""")
        print("Table has now been created")


    
    

