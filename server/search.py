#!/usr/bin/env python

import cgi
import functools
import json
import sys
import traceback

import util.search, util.db, util.load, util.save

def jsond ():
    print "Content-type: application/json"
    print

def jsonw (f):
    @functools.wraps(f)
    def jsonw (*args, **kwargs):
        jsond()
        f(*args, **kwargs)

    return jsonw

def xml (fn):
    print """Content-type: application/xml; name=%s""" % fn
    print """Content-disposition: attachment; filename=%s""" % fn
    print

def html ():
    print """Content-type: text/html"""
    print

def textarea (f):
    @functools.wraps(f)
    def textarea (*args, **kwargs):
        html()
        print "<textarea>"
        f(*args, **kwargs)
        print "</textarea>"

    return textarea

@jsonw
def search (args, cgi_args, lexicon):
    search_term = cgi_args.getfirst("s", None)

    if search_term is None:
        return

    search_term = util.search.SearchList.fromjson(search_term)

    result = lexicon.search(search_term, show_query=False)

    print json.dumps(result)

@jsonw
def challenge (args, cgi_args, lexicon):
    challenge_words = cgi_args.getfirst("w", None)

    if challenge_words is None:
        return

    words = set(json.loads(challenge_words))

    result = lexicon.challenge(words)

    print json.dumps(result)

@textarea
def load (args, cgi_args, lexicon):
    fileitem = cgi_args["d"]

    if fileitem is None:
        return

    if fileitem.file:
        cont = fileitem.file.read()
        s = util.load.parse_search(cont)
        print s.asjson()
        return

    print json.dumps("Nothing.")   

def save (args, cgi_args, lexicon):
    search_term = cgi_args.getfirst("v", None)

    if search_term is None:
        return

    xml("search.zzs")
    print util.save.search_list_to_xml(util.search.SearchList.fromjson(search_term))

def main (args, cgi_args):
    if not (cgi_args.has_key("s") or cgi_args.has_key("w") or cgi_args.has_key("v") or cgi_args.has_key("d")):
        jsond()
        print json.dumps("No search terms provided.")
        return

    lexicon = cgi_args.getfirst("lexicon", None)

    if lexicon is None:
        lexicon = cgi_args.getfirst("l", None)

    if lexicon is None:
        jsond()
        print json.dumps("No lexicon provided.")
        return

    lex = util.db.lexicon(lexicon)

    if lex is None:
        jsond()
        print json.dumps("Invalid lexicon '%s'" % lexicon)

    if cgi_args.has_key("d"):
        return load(args, cgi_args, lex)
    elif cgi_args.has_key("v"):
        return save(args, cgi_args, lex)
    elif cgi_args.has_key("s"):
        return search(args, cgi_args, lex)
    elif cgi_args.has_key("w"):
        return challenge(args, cgi_args, lex)
    else:
        jsond()
        print json.dumps("Nothing.")

if __name__=="__main__":
    sys.stderr=sys.stdout

    try:
        main (sys.argv, cgi.FieldStorage())
    except Exception, e:
        jsond()

        print json.dumps({"exception_type": e.__class__.__name__, "exception_message": str(e)})
        
