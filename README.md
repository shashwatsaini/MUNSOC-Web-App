# The Web App for The Model United Nations Society, Dayananda Sagar University
Made using Flask, SQLAlchemy.

## Installation
1. Install all python packages in requirements.txt.
2. Setup Google-Oauth & relevant keys to synchronize database with GDrive.
3. Setup SMTP login keys, a mail transfer protocol, to send automatic mails upon registration.
4. Run app.py for debugging.

It might be easier to run this app without GDrive functionality if you wish to contribute, to do so set FLAG_gdrive to False in app.py.

You could also disable the mailing service, to do so set FLAG_mail to False in app.py. See Development Notes for more info.

## Development Notes

### Frameworks Used

1. Flask | [docs](https://flask.palletsprojects.com/en/3.0.x/)
2. Flask-SQLAlchemy | [docs](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
3. Bootstrap | [docs](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
4. Google API Client | [docs](https://github.com/googleapis/google-api-python-client/blob/main/docs/README.md)
5. Simple Mail Transfer Protocol (SMTP) | [docs](https://docs.python.org/3/library/smtplib.html)

### Folder Setup

```shell
├── application
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── models.py
├── app.py
├── db_directory
│   └── database.sqlite3
├── LICENSE
├── README.md
├── requirements.txt
├── static
│   ├── img
│   ├── logo_white_notext.svg
│   ├── logo_white.png
│   ├── Museo.otf
│   ├── MuseoSans.otf
│   ├── separator2.png
│   ├── seperator.png
│   └── style.css
├── teams.csv
└── templates
    ├── events.html
    ├── home.html
    ├── register.html
    └── secretariat.html
```

If you wish to contribute to frontend, you would only need to focus on templates & static folders.

For backend, you would be focusing on all folders in the structure.

### Robust Database Implementation
The app implements a highly safe database to collect registration data, that is continuously being synchronized across three layers:

1. The database itself.
2. CSV file in root directory.
3. GDrive.

GDrive synchronization is extremely important for the purposes of this app, to access information easily without connecting to the corresponding cloud-hosted server setup.

### Logging Implementation with Flask

The app also includes an extensive logging setup. All initializations, requests, and GDrive statuses are constantly logged into webapp.log in root directory.

### Google API Client & SMTP Notes

Google API Client uses a service account key in .json format, that you can get from 'Google Cloud Platform -> Service Account.' Refer to docs here: [Service Accounts Overview](https://cloud.google.com/iam/docs/service-account-overview).
Rename this key to 'gcp_key.json' and add it to the root directory, to enable GDrive synchronization, an important process for the upkeep of the app.

SMTP uses simple email and password features to login. To use with gmail, you must set 'smtp' variable in 'applications/controllers.py' to 'smtplib.SMTP('smtp.gmail.com', 587).'
Follow the docs to connect other service providers: [SMTP docs](https://docs.python.org/3/library/smtplib.html).

Our implementation makes use of a key in 'gmail_key.txt' with the syntax:
```shell
email:<add email here>
password:<add app code here>
```
App code here refers to the app code for Gmail / Google accounts, that can be generated through 'Security -> 2 Factor Authentication' tab. Normal login passwords do not work.

## Copyright

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/

