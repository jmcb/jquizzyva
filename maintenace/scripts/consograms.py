#!/usr/bin/env python
"""
This script creates a new column in the database consisting of consograms, as
well as an index for that column.
"""

import sqlite3
import sys
import util.consogram

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

    print "Creating new temporary table...", 

    con.create_function("make_consogram", 1, util.consogram.consogram)

    con.execute("DROP TABLE IF EXISTS temp_words")

    con.execute("CREATE TABLE temp_words (word varchar(16), length integer, playability integer, playability_order integer, min_playability_order integer, max_playability_order integer, combinations0 integer, probability_order0 integer, min_probability_order0 integer, max_probability_order0 integer, combinations1 integer, probability_order1 integer, min_probability_order1 integer, max_probability_order1 integer, combinations2 integer, probability_order2 integer, min_probability_order2 integer, max_probability_order2 integer, alphagram varchar(16), num_anagrams integer, num_unique_letters integer, num_vowels integer, point_value integer, front_hooks varchar(32), back_hooks varchar(32), is_front_hook integer, is_back_hook integer, lexicon_symbols varchar(16), definition varchar(256), consogram varchar(17));")

    print "Done!"

    con.execute("DROP TABLE IF EXISTS consograms")

    con.execute("CREATE TABLE consograms (alphagram varchar(16), consogram varchar(17))")

    print "Done!"

    print "Populating consogram table...",

    con.execute("INSERT INTO consograms SELECT DISTINCT alphagram, make_consogram(alphagram) FROM words")

    con.execute("CREATE INDEX consogram_index ON consograms (consogram)")

    print "Done!"

    print "Populating temp table...",

    con.execute("insert into temp_words select words.word, words.length, words.playability, words.playability_order, words.min_playability_order, words.max_playability_order, words.combinations0, words.probability_order0, words.min_probability_order0, words.max_probability_order0, words.combinations1, words.probability_order1,words.min_probability_order1, words.max_probability_order1, words.combinations2, words.probability_order2, words.min_probability_order2, words.max_probability_order2, words.alphagram, words.num_anagrams, words.num_unique_letters, words.num_vowels, words.point_value, words.front_hooks, words.back_hooks, words.is_front_hook, words.is_back_hook, words.lexicon_symbols, words.definition, consograms.consogram from words join consograms on consograms.alphagram=words.alphagram;")

    print "Done!"

    print "Dropping current words table...",

    con.execute("DROP TABLE words")

    print "Renaming temp table..."

    con.execute("ALTER TABLE temp_words RENAME TO words")

    print "Recreating indices...", 

    print "play_index ...",

    con.execute("CREATE UNIQUE INDEX play_index on words (length, playability_order);")

    print "play_min_max_index ...",

    con.execute("CREATE INDEX play_min_max_index on words (length, min_playability_order, max_playability_order);")

    print "prob0_index ...",

    con.execute("CREATE UNIQUE INDEX prob0_index on words (length, probability_order0);")

    print "prob0_min_max_index ...",

    con.execute("CREATE INDEX prob0_min_max_index on words (length, min_probability_order0, max_probability_order0);")

    print "prob1_index ...",

    con.execute("CREATE UNIQUE INDEX prob1_index on words (length, probability_order1);")

    print "prob1_min_max_index ...",

    con.execute("CREATE INDEX prob1_min_max_index on words (length, min_probability_order1, max_probability_order1);")

    print "prob2_index ...",

    con.execute("CREATE UNIQUE INDEX prob2_index on words (length, probability_order2);")

    print "prob2_min_max_index ...",

    con.execute("CREATE INDEX prob2_min_max_index on words (length, min_probability_order2, max_probability_order2);")

    print "word_alphagram_index ...",

    con.execute("CREATE INDEX word_alphagram_index ON words (alphagram);")

    print "word_back_hook_index ...",

    con.execute("CREATE INDEX word_back_hook_index ON words (is_back_hook);")

    print "word_front_hook_index ...",

    con.execute("CREATE INDEX word_front_hook_index ON words (is_front_hook);")

    print "word_index ...", 

    con.execute("CREATE UNIQUE INDEX word_index ON words (word);")

    print "word_length_index ...",

    con.execute("CREATE INDEX word_length_index ON words (length);")

    print "word_consogram_index ...",

    con.execute("CREATE INDEX word_consogram_index ON words (consogram);")

    print "Done!"

    print "Dropping consograms table ...",

    con.execute("DROP TABLE IF EXISTS consograms")

    print "Done!"

    print "Vacuuming database."

    con.execute("VACUUM")

    con.commit()

    print "Done! Closing database!"

    con.close()

if __name__=="__main__":
    main(sys.argv)
