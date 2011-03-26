#!/usr/bin/env python

import cgi
import json
import sys

import util.search, util.db

def main (args, cgi_args):
    search_term = cgi_args.getfirst("term", None)

    if search_term is None:
        search_term = cgi_args.getfirst("s", None)

    if search_term is None:
        print json.dumps("No search term provided.")
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

    search_term = util.search.SearchList.fromjson(search_term)

    result = lex.search(search_term, show_query=False)

    print json.dumps(result)    

if __name__=="__main__":
    sys.stderr=sys.stdout

    print "Content-type: application/json"
    print

    try:
        main (sys.argv, cgi.FieldStorage())
    except Exception, e:
        print json.dumps({"exception_type": e.__class__.__name__, "exception_message": str(e)})
        
