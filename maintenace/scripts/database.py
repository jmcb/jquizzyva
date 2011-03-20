#!/usr/bin/env python
"""
This script may result in database queries for Anagrams and Subanagrams being
faster, as they create a new index on the alphagram column. It is not necessary
that you run this script! However, while it modifies the database and will
increase its size, the same database should still run properly with Zyzzyva!

Zyzzyva's standard CSW database goes from about 109mb to 119mb with the new
indexes this script creates.
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

    print "Creating new indexes... ", 

    con.execute("CREATE INDEX word_alphagram_index ON words (alphagram)")

    print "alphagrams ... ", 

    con.execute("CREATE INDEX word_front_hook ON words (is_front_hook)")

    print "front hooks ... ",

    con.execute("CREATE INDEX word_back_hook ON words (is_back_hook)")

    print "back hooks ... done!"

    print "Vacuuming database."

    con.execute("VACUUM")

    con.commit()

    print "Done! Closing database!"

    con.close()

if __name__=="__main__":
    main(sys.argv)
