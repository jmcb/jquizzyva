#!/usr/bin/env python

import cgi
import json
import sys
import traceback

import util.search, util.db

def main (args, cgi_args):
    search_term = cgi_args.getfirst("term", None)

    if search_term is None:
        search_term = cgi_args.getfirst("s", None)

    challenge_words = cgi_args.getfirst("words", None):
    
    if challenge_words is None:
        challenge_words = cgi_args.getfirst("w", None)

    if search_term is None and challenge_words is None:
        print json.dumps("No search terms provided.")
        return

    lexicon = cgi_args.getfirst("lexicon", None)

    if lexicon is None:
        lexicon = cgi_args.getfirst("l", None)

    if lexicon is None:
        print json.dumps("No lexicon provided.")
        return

    lex = util.db.lexicon(lexicon)

    if lex is None:
        print json.dumps("Invalid lexicon '%s'" % lexicon)

    if search_term is not None:
        search_term = util.search.SearchList.fromjson(search_term)

        result = lex.search(search_term, show_query=False)

        print json.dumps(result)
    else:
        words = json.loads(challenge_words)

        result = lex.challenge(*challenge_words)

        print json.dumps(result)

if __name__=="__main__":
    sys.stderr=sys.stdout

    print "Content-type: application/json"
    print

    try:
        main (sys.argv, cgi.FieldStorage())
    except Exception, e:
        print json.dumps({"exception_type": e.__class__.__name__, "exception_message": str(e), "exception_traceback": traceback.format_exc()})
        
