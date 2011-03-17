*********
jQuizzyva
*********

While this does not aim to have anywhere near the complete functionality of
`Zyzzyva`_, it does aim to provide a relatively simple interface to the Zyzzyva
database, allowing for querying and so-on. It will not include cardbox and
other such functionality, primarily because I do not use these, but also
because that would obligate a layer of persistence and user log-ins.

Server
======

The interface "serving" the Zyzzyva database will be written in Python, and
will be a CGI-based JSON service. Thus, while POST and GET access is available,
all the results will be returned as plain JSON.

In future, this may be extended to serve as a JSON-RPC-based server instead,
but for the time being this will hopefully suffice.

Interface
=========

The initial interface will be written with jQuery and jQuery UI in mind; these
will have access to the information in the database via AJAX, and this
information will be presented in a (hopefully) clean manner to the user.

Initial to-do list consists on the following:

 1. "Search" option, using all of the options presented in the current Zyzzyva
    interface.
 2. "Adjudication" option, providing a similar interface to the current Zyzzyva
    "Word Judge" interface.
 3. A "Quiz" mode, which will present a series of words, defined by a search
    term of your own chosing, but also including randomly generated words which
    are not allowable in your chosen lexicon.

The primary lexicon choice will be SOWPODS, via CSW; this data package will not
be included in the software for licensing reasons. To generate this database,
you will need to install a copy of Zyzzyva and select the lexicon desired; once
it has generated, you will find a copy in ~/Zyzzyva, where the lexicon file is
ACRONYM.db.

License
=======

All of the code, where applicable, is licensed under the terms of the MIT
License; furhter information on this subject can be found in the COPYING.rst
file.

.. Links:
.. _`Zyzzyva`: http://www.zyzzyva.net/
