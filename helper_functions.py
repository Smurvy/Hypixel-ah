from tabnanny import check
import requests
import sqlite3

def getJson(pageNum,endpoint="auctions"):
    r = requests.get("https://api.hypixel.net/skyblock/" + endpoint + f"?page={pageNum}")
    return r.json()

def convertFromUUIDtoUsername(uuid):
    data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
    print(data["name"])

def checkIfTableExists(cur, tableName, tableType):
    # check if the table exists
    try:
        cur.execute(f"SELECT * FROM {tableName}")
        return True

    except sqlite3.OperationalError:
        # the simple and expanded paramaters are just there to create two different
        # tables, the expanded one is used for active auctions and 
        # the simple one is used for past auctions
        if tableType == "expanded":
            cur.execute(f""" CREATE TABLE {tableName} (
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
        elif tableType == "simple":
            # this essentaily just makes sure than when I run "past_auctions.py"
            # it still works - this isn't entirely necessary if you only run from the main
            # python file
            checkIfTableExists(cur,"currentAuctions","expanded")
            cur.execute(f""" CREATE TABLE {tableName} (
                                itemName TEXT);""")
                                #itemPrice INTEGER) - add this back in later
            print("Table has now been created")


def registerItem(cur):
    # take each uniqe item in the database and register it in the "past Auctions database"
    itemNameList = []
    getJson(0,"auctions_ended")
    itemNameTup = cur.execute("SELECT itemName FROM currentAuctions;")
    for item in itemNameTup:
        if item not in itemNameList:
            itemNameList.append(tuple([item[0]]))
    return itemNameList
        
    



    
    

