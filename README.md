#rebooru

This is going to eventually, hopefully, be a django booru with a deep tagging and search system.

###QUICK INSTALL

If you're installing this for some reason, the only requirements are django and south; you can use whatever database/server setup you want

I've included a gunicorn config just because I use it, but it's not like that's all it works with or anything!!

As a note, the SECRET\_KEY setting will auto-generate the first time you run it, and get saved to a file and imported from that in the future. This is to avoid multiple servers using the same key, or revealing it accidentally (the file is in .gitignore).
