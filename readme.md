Marvin
---------

Python bot for fun and usefulness.
Got it's attitude from the Hitchhiker's Guide to the Galaxy

Got it's roots from pyFlowbot and Phenny and a few other distant cousins.

Now it's own bot.

-To use
copy core/config.copy.py to core/config.py and update logins and passwords (to use flowdock and any authenticated apis like github)
mark bot.py as executable or just run with python:
$ python bot.py

add argument to determine adapter (where input and output come from).  Currently only accepts flowbot (flowdock) and console
$ python bot.py -a flowbot

when all else fails
$ python bot.py -h

--Storage
Storage module uses redis, so unless you change that, you should have redis running on the default settings.