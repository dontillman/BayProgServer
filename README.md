# bayprog

Copyright 2021 to 2024, J. Donald Tillman.  All rights reserved.

This is the source code for the BayProg.org web site, implemented in
Django / Python.

BayProg is the San Francisco Bay Area Progressive Rock web site,
containing all sorts of resources for progressive rock musicians and
fans.  Basically Don's roladex.  Established in 1999, I believe it was
the first web site for local support of a serious music genre.

The BayProgProject is the overall package.  You will need to add some
files specific to your server setup (settings.py and asgi.py or
wsgi.py).  These are generated automatically by Django, but you need
to tweak them.

The BayProgApp module is the main web implementation.  It supports:
    * The Home page
    * Bands and Musicians
    * Events
    * Venues
    * Albums
    * Music Stores
    * Instrument Makers
    * Instrument Repair
    * Equipment Makers
    * Record Stores
    * And a Message Board

Cities are included in the database so that venues, stores, and such,
can be organized by region.

The BayProgUser module is pretty standard.  The only interesting thing
is that there are intentionally no user ids like "hitler3000"' just
email addresses and real names.

You will need an email account to sign up users for the message board.

Happy to help or answer questions.

  — Don
