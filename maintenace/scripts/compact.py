#!/usr/bin/env python
"""
There is no need to run this script! jQuizzyva will run fine without
alterations to the Zyzzyva database. However, in order to reduce the file size
if you wish, you can run this script!

NOTE: Modifying a database with this script will cause it to cease functioning
with Zyzzyva.

The standard CSW database goes from about 109mb to 69mb with this script.
"""

import sqlite3
import sys

def main (args):
    if not args:
        print "usage: compact.py <database file>"
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

    con.execute("""CREATE TABLE temp_words (
        word varchar(16),
        length integer,
        alphagram varchar(16),
        num_anagrams integer,
        num_unique_letters integer,
        num_vowels integer,
        point_value integer,
        front_hooks varchar(32),
        back_hooks varchar(32),
        is_front_hook integer,
        is_back_hook integer,
        lexicon_symbols varchar(16),
        definition varchar(256))""")

    print "Created new table, ok!"

    print "Transferring data from words into temp_words..."

    con.execute("INSERT INTO temp_words SELECT word, length, alphagram, num_anagrams, num_unique_letters, num_vowels, point_value, front_hooks, back_hooks, is_front_hook, is_back_hook, lexicon_symbols, definition FROM words")
    con.commit()

    print "Done!"

    print "Dropping old word table..."

    con.execute("DROP TABLE words")

    print "Renaming temp_words to words..."

    con.execute("ALTER TABLE temp_words RENAME TO words")

    print "Creating new indexes... ", 

    con.execute("CREATE UNIQUE INDEX word_index ON words (word)")

    print "words ... ",

    con.execute("CREATE INDEX word_length ON words (length)")

    print "lengths ...",

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
