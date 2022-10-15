from re import L
import helper_functions as h
import sqlite3
import current_auctions as ca
from datetime import datetime

class Item():

    # used to convert epoch/unix time -> a date later in the program - turns out the API returns the epoch/unix time
    # in milliseconds it will throw an error unless there is a division of 1000 at some point
    def convertDate(self,ty):
        try:
            convertedDate = datetime.fromtimestamp(ty/1000)
            formattedDate = convertedDate.strftime('%Y-%m-%d %H:%M:%S')

            return formattedDate

        except OSError:
            print(ty)

    
    def __init__(self, itemName,tier,startDate, endDate, category, startingBid, isBin, bids,auctioneer):
        self.itemName = itemName
        self.tier = tier
        self.startDate = self.convertDate(startDate)
        self.endDate = self.convertDate(endDate)
        self.category = category
        self.startingBid = startingBid
        self.isBin = isBin
        self.bids = bids
        self.auctioneer = auctioneer


    # Mojangs API is particularly slow, so don't use this method unless you aboslutely need to get a username
    def getUsernames(self):
        h.convertFromUUIDtoUsername(self.auctioneer)

    # bids are return with a bunch of extra info, I just want the prices
    def pullBidData(self, biddersList):
        priceList = []
        for x in range(len(biddersList)):
            priceList.append(biddersList[x]['amount'])
        return priceList

    def returnAsTuple(self):
        return (self.itemName,self.tier,self.startDate,self.endDate,self.category,self.startingBid,self.isBin,self.bids,self.auctioneer)

    def printInfo(self):
        print("Item Name: " + self.itemName)
        print("Item Tier: " + self.tier)
        print("Item Category: " + self.category)
        print("Item isBin: " + str(self.isBin))

        # These date values are returned in epoch time; needed to convert them
        print("Item Start Date: " + str(self.convertDate(self.startDate)))
        print("Item End Date: " + str(self.convertDate(self.endDate)))

        print("Item Price (listed at): ¢" + str(self.startingBid))
        print(self.bids)
    
        print()

# i just want the current highest bid, not the bid history - could be a feature for later implementation
def getHighestBid(listOfBids):
    # in case the ltem is actually a part of a bin 
    if len(listOfBids) == 0:
        return 0
    else:
        return listOfBids[-1]['amount']

def getItemsAndWriteToDb():
    response = h.getJson(0)
    numPages = response['totalPages']

    con = sqlite3.connect("Auctions")
    cur = con.cursor()
    h.checkIfTableExists(cur)


    for x in range(numPages - 1):
        print(x)
        listOfObjs = []
        
        # I was having an issue where the number of items wouldn't be divisible by
        # 1000, so I implemeneted this
        itemsOnPage = 1000

        if x == numPages:
            itemsOnPage = itemsOnPage % 1000

        response = h.getJson(x)
        response = response['auctions']

        for x in range(itemsOnPage):
            currentItem = response[x]
            obj = Item(currentItem['item_name'],
                    currentItem['tier'],
                    currentItem['start'],
                    currentItem['end'],
                    currentItem['category'],
                    currentItem['starting_bid'],
                    currentItem['bin'], 
                    getHighestBid(currentItem['bids']),
                    currentItem['auctioneer'])
            
            # I return as tuples because that is what the sqlite wants in order to 
            # put into a database
            listOfObjs.append(obj.returnAsTuple())
        query = cur.executemany("INSERT INTO currentAuctions VALUES (?,?,?,?,?,?,?,?,?)", listOfObjs)

    # setting up connection to currentAuctions db
    
    # ensure that the table inside of the database exists, if it doesn't it creates it
    h.checkIfTableExists(cur)

    

    query = cur.execute("SELECT * FROM currentAuctions")

    for x in query:
        print(x)

    con.commit()
    con.close
