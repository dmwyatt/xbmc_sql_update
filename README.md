xbmc_sql_update
===============

A python script to help update the XBMC (Kodi) MySQL library when you move some or all of your files to a new location.

Installation
============

Put script wherever you want.  If you have `pip`, then just run `pip install -r requirements.txt`.  Otherwise, install the packages listed in `requirements.txt`.

Usage
=====

Run `xbmc_sql_update.py -h` for help.

If you moved all of your media:

    xbmc_sql_update.py smb://old_server/old_path/ smb://new_server/new_path/your_momma/whatever/ mysql_host mysql_user mysql_password

If you moved just some of your folders to a new location:

    xbmc_sql_update --folders "Star Trek, Star Trek: TNG, Star Trek: DS9" smb://old_server/old_path/ smb://new_server/new_path/your_momma/whatever/ mysql_host mysql_user mysql_password
    
If you moved a lot of folders to a new location, but not all of them:

    xbmc_sql_update --folders some_file_name.txt smb://old_server/old_path/ smb://new_server/new_path/your_momma/whatever/ mysql_host mysql_user mysql_password

Where some_file_name.txt contains a list of folders.  One folder per line.
