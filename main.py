import active_auctions as aa
import sqlite3
import helper_functions as h

def main():
    # gets all current items on the auction house and puts them in a database
    con = sqlite3.connect("Auctions")
    cur = con.cursor()
    h.checkIfTableExists(cur,"currentAuctions","expanded")
    
    # gets all current items on the auction house and puts them in a database
    aa.getItemsAndWriteToDb(cur)


    con.commit()
    con.close
main()