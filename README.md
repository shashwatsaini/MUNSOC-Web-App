# The Web App for The Model United Nations Society, Dayananda Sagar University
Made using Flask, SQLite.

## Installation
Install all python packages in requirements.txt.
Run flask_app.py for debugging.
It is recommended you setup Google SDK, Google-Oauth, & relevant keys as well, to synchronize database with GDrive. Otherwise, simply remove all GDrive helper functions.
Run app.py for debugging.

## Robust Database
The app implements a highly safe database to collect registration data, that is continuously being synchronized across three layers:
1. The database itself.
2. CSV file in root directory.
3. GDrive.

## Copyright

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/

