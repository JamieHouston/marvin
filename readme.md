Marvin
---------

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/foresterh/marvin?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)  (opens in same tab)

Python bot for fun and usefulness.

Got it's attitude from the Hitchhiker's Guide to the Galaxy

Got it's roots from pyFlowbot and Phenny and a few other distant cousins.

Now it's own bot.

Works (mostly) with python 3.4.  No guarantee for earlier (or 2.*) versions

-To use
(optionally) install and run redis (in separate tab)

``` $ brew install redis ```

``` $ redis-server ```

install pip

``` sudo easy_install pip ```

install requirements

``` $ sudo pip install -r requirements.txt ```

copy core/config.copy to ./config and update logins and passwords (to use flowdock and any authenticated apis like github)

    $ cp core/config.copy config

mark bot.py as executable or just run with python:

    $ python bot.py

add argument to determine adapter (where input and output come from).  Currently only accepts flowbot (flowdock) and console

    $ python bot.py -a console

when all else fails
     
``` $ python bot.py -h ```

--Storage
Storage module uses redis, so unless you change that, you should have redis running on the default settings.
