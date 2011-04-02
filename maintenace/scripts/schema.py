#!/usr/bin/env python
"""
This script prints out the schemae of the relevant databases.
"""

import sqlite3
import sys

def main (args):
    if not args:
        print "usage: database.py <database file>"
        return

    while len(args) != 1:
        args.pop(0)

    db = args[0]

    print "Working on database %s..." % db

    try:
        con = sqlite3.connect(db)
    except:
        print "Couldn't connect to %s!" % db
        return

    cur = con.execute("SELECT sql FROM sqlite_master")

    result = cur.fetchall()
    
    print "\n".join([res[0] for res in result])

    con.close()

if __name__=="__main__":
    main(sys.argv)
