import os
import logging
from datetime import datetime
from flask import current_app as app
from flask import Flask, request
from flask import render_template, request, redirect, url_for
from application.database import db
from application.models import Teams
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

drive_service = None
gdrive_sync = False

@app.route('/')
def home():
	app.logger.info(f'[{datetime.now()}] GET: home.html')
	return render_template('home.html')

@app.route('/events')
def events():
	app.logger.info(f'[{datetime.now()}] GET: events.html')
	return render_template('events.html')

@app.route('/the-secretariat')
def secretariat():
	app.logger.info(f'[{datetime.now()}] GET: secretariat.html')
	return render_template('secretariat.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	global drive_service

	if request.method == 'GET':
		app.logger.info(f'[{datetime.now()}] GET: register.html')
		return render_template('register.html', registered=False)
	else:
		try:
			email = request.form['inputEmail']
			name = request.form['inputTeamName']
			committee_pref = int(request.form['inputCommitteePreference'])
			size = int(request.form['inputTeamSize'])
			member_name_1 = request.form['inputMemberName1']
			member_name_2 = request.form['inputMemberName2']
			member_name_3 = request.form['inputMemberName3']

			if size == 4:
				member_name_4 = request.form['inputMemberName4']
				team = Teams(email=email, name=name, committee_pref=committee_pref, size=size, member_name_1=member_name_1, member_name_2=member_name_2, member_name_3=member_name_3, member_name_4=member_name_4)
			else:
				team = Teams(email=email, name=name, committee_pref=committee_pref, size=size, member_name_1=member_name_1, member_name_2=member_name_2, member_name_3=member_name_3)

			app.logger.info(f'[{datetime.now()}] POST: Received registration info')

			db.session.add(team)
			db.session.commit()

			app.logger.info(f'[{datetime.now()}] POST: Committed to database')

			data = Teams.query.all()
			data_dicts = [{'id': item.id, 'email': item.email, 'name': item.name, 'committee_pref': item.committee_pref,
			'size': item.size, 'member_name_1': item.member_name_1, 'member_name_2': item.member_name_2,
			'member_name_3': item.member_name_3, 'member_name_4': item.member_name_4} for item in data]
			df = pd.DataFrame(data_dicts)
			df.to_csv('teams.csv')

			app.logger.info(f'[{datetime.now()}] POST: Exported database to csv')

			synchronize_drive('teams.csv')

			app.logger.info(f'[{datetime.now()}] POST: Synchronized to GDrive')

			return render_template('register.html', registered=True)

		except Exception as e:
			app.logger.exception(f'[{datetime.now()}] POST: Exception has occured.')
			app.logger.exception(f'[{datetime.now()}] POST: {e}')
			return redirect('/')

# Authentication for GCP
def auth(key, FLAG_gdrive):
	global drive_service, gdrive_sync
	gdrive_sync = FLAG_gdrive

	if gdrive_sync:

		SCOPES = ['https://www.googleapis.com/auth/drive']
		SERVICE_ACCOUNT_FILE = key

		credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
		drive_service = build('drive', 'v3', credentials=credentials)

		app.logger.info(f'[{datetime.now()}] Google Auth & GDrive Services successful')

		return drive_service

	else: 
		app.logger.info(f'[{datetime.now()}] Google Auth & GDrive Services are disabled')
		return None

# Get or create folder in GDrive
def get_or_create_folder(folder_name):
    # Search for the folder by name
    response = drive_service.files().list(q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
      spaces='drive',
      fields='files(id)').execute()
    folders = response.get('files', [])

    if folders:
        folder_id = folders[0]['id']
        add_folder_permission(folder_id)
        app.logger.info(f'[{datetime.now()}] GDrive: Folder {folder_name} found with ID: {folder_id}')
        return folder_id
    else:
    	# Create the folder
        app.logger.exception(f'[{datetime.now()}] GDrive: No folder named {folder_name} found. Creating one.')
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=file_metadata,
           fields='id').execute()
        folder_id = folder.get('id')
        add_folder_permission(folder_id)
        app.logger.exception(f'[{datetime.now()}] GDrive: Folder {folder_name} created with ID: {folder_id}')
        return folder_id

# Add folder permissions to view the folder in GDrive UI
def add_folder_permission(folder_id, role='writer'):
    permission = {
        'type': 'anyone',
        'role': role
    }

    drive_service.permissions().create(fileId=folder_id, body=permission).execute()
    app.logger.info(f'[{datetime.now()}] GDrive: Added anyone-writer permissions to Folder')

# Synchronize the csv format of the database with GDrive
def synchronize_drive(file_path, folder_name='MUNSOC Web App'):
	if gdrive_sync:
	    folder_id = get_or_create_folder(folder_name)
	    
	    # Search for the existing file in the folder
	    response = drive_service.files().list(q=f"name='{os.path.basename(file_path)}' and '{folder_id}' in parents",
	                                          fields='files(id)').execute()
	    files = response.get('files', [])
	    
	    if files:
	        file_id = files[0]['id']
	        # Update the existing file
	        media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=True)      
	        file = drive_service.files().update(fileId=file_id, media_body=media).execute()
	        app.logger.info(f'[{datetime.now()}] GDrive: File {os.path.basename(file_path)} updated in folder {folder_name}')
	    else:
	        # Create the file if it doesn't exist
	        file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
	        media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=True)      
	        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	        app.logger.info(f'[{datetime.now()}] GDrive File {os.path.basename(file_path)} created in folder {folder_name}')

	else:
		app.logger.info(f'[{datetime.now()}] GDrive: Sync is disabled')	


