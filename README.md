# bayprog
BayProg.org web site, implemented in Django

Copyright 2021 to 2023, J. Donald Tillman.  All rights reserved.

BayProg is the San Francisco Bay Area Progressive Rock web site.
It contains all sorts of resource for progressive rock musicians
and fans.  Basically Don's roladex.

The project is the overall package.
The app module is the web implementation.
The user module is keeps the user implementation independent.

The bayprog app handles the home page, bands and musicians, 
events, venues, albums, music stores, instrument makers, 
instrument repair, equipment makers, record stores, and a 
message board.


The user module is pretty standard.  The only interesting thing 
is that there are intentionally no user ids like "hitler3000", 
just emails and real names.  And admin status.
