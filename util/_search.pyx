import util.pattern, util._pattern

CALLBACK_FUNCTION = "callback"

cdef class AnagramMatchBase (object):
    cdef object cpatternobj
    cdef object patternobj
    cdef public object search_string
    cdef public bint negated

    def __init__ (AnagramMatchBase self, object search_string, bint negated = False):
        self.search_string = search_string
        self.negated = negated

    cpdef object clause (self):
        return CALLBACK_FUNCTION

    def pattern (self):
        if self.patternobj == None:
            self.patternobj = util.pattern.Pattern.fromstring(self.search_string)
            self.cpatternobj = self.patternobj.as_cpattern()

        def search_function (char* word):
            return util._pattern.try_word(self.cpatternobj, word)

        return search_function

    cpdef object bounds (self):
        return self.patternobj.bounds()

cdef class SubanagramMatchBase (object):
    cdef object cpatternobj
    cdef object patternobj
    cdef public object search_string
    cdef public bint negated

    def __init__ (SubanagramMatchBase self, object search_string, bint negated = False):
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
