from atexit import register
import helper_functions as h
import sqlite3


def pastAuctions():
    # creation + connection to database
    con = sqlite3.connect("Auctions")
    cur = con.cursor()

    # safety check to make sure that the table exists
    h.checkIfTableExists(cur, "pastAuctions","simple")

    itemTuple = h.registerItem(cur)
    cur.executemany("INSERT INTO pastAuctions VALUES (?);", itemTuple)

    
    con.commit()
    con.close()
pastAuctions()


# I want the following information in my data base
    # - Item price lifetime
    #   Just take the amount sold and add the price it just sold a
    # - Time sold at
    #   - To determine how many/what price something was sold in the last
    #     x time period simply make an expression asking
    #     <current_time> - <days,months, etc.>
    # - item tier -> to determine if the item is recombed or not
    #   use a boolean?
    # - If it was a bin listing
    # - Time sold at 
