import util.pattern, util._pattern

CALLBACK_FUNCTION = "callback"

def alphagram (string):
    """
    This converts a string into an 'alphagram': an alphabetically sorted string.
    """
    return "".join(sorted(list(string.upper())))

cdef class AnagramMatch (object):
    cdef object cpatternobj
    cdef object patternobj
    cdef object search_string
    cdef bint negated

    def __init__ (AnagramMatch self, object search_string, bint negated = False):
        self.search_string = search_string
        self.negated = negated

    cpdef object clause (self):
        if "?" in self.search_string or "[" in self.search_string or "*" in self.search_string:
            return CALLBACK_FUNCTION

        ag = alphagram(self.search_string)

        return ("words.alphagram=?", (ag, ))

    def pattern (self):
        if self.patternobj == None:
            self.patternobj = util.pattern.Pattern.fromstring(self.search_string)
            self.cpatternobj = self.patternobj.as_cpattern()

        def search_function (char* word):
            return util._pattern.try_word(self.cpatternobj, word)

        return search_function

    cpdef object bounds (self):
        return self.patternobj.bounds()

cdef class SubanagramMatch (object):
    def __init__ (SubanagramMatch self, object search_string, bint negated = False):
        self.search_string = search_string
        self.negated = negated

    cpdef object clause (self):
        return CALLBACK_FUNCTION

    def pattern (self):
        if self.patternobj == None:
            self.patternobj = util.pattern.SubPattern.fromstring(self.search_string)
            self.cpatternobj = self.patternobj.as_cpattern()

        def search_function (char* word):
            return util._pattern.try_word(self.cpatternobj, word)

        return search_function

    cpdef object bounds (self):
        return self.patternobj.bounds()

