from re import L
import helperFunctions as h
from datetime import datetime


class Item():

    def __init__(self, itemName,tier,startDate, endDate, category, startingBid, isBin, bids):
        self.itemName = itemName
        self.tier = tier
        self.startDate = startDate
        self.endDate = endDate
        self.category = category
        self.startingBid = startingBid
        self.isBin = isBin
        self.bids = bids
        
    # used to convert epoch/unix time -> a date later in the program - turns out the API returns the epoch/unix time
    # in milliseconds it will throw an error unless there is a division of 1000 at some point
    def convertDate(self,ty):
        try:
            convertedDate = datetime.fromtimestamp(ty/1000)
            formattedDate = convertedDate.strftime('%Y-%m-%d %H:%M:%S')

            return formattedDate

        except OSError:
            print(ty)


    def printInfo(self):
        print("Item Name: " + self.itemName)
        print("Item Tier: " + self.tier)
        print("Item Category: " + self.category)
        print("Item isBin: " + str(self.isBin))

        # These date values are returned in epoch time; needed to convert them
        print("Item Start Date: " + str(self.convertDate(self.startDate)))
        print("Item End Date: " + str(self.convertDate(self.endDate)))

        print("Item Price: ¢" + str(self.startingBid))
        # print("Item List of Bids: " + self.bids)
        print()

def main():
    
    response = h.getJson()
    response = response['auctions']

    


    for x in range(1000):
        print(x + 1)
        currentItem = response[x]
        obj = Item(currentItem['item_name'],
                   currentItem['tier'],
                   currentItem['start'],
                   currentItem['end'],
                   currentItem['category'],
                   currentItem['starting_bid'],
                   currentItem['bin'],
                   currentItem['bids'])
                   
        obj.printInfo()
        del obj

        print(response[x]['auctioneer'])
        
    
main()


