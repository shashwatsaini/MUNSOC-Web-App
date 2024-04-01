import os
from flask import Flask
from flask import redirect, url_for, render_template
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import Teams

current_dir = os.path.abspath(os.path.dirname(__file__))
app = None

# Creating the web app
def create_app():
	app = Flask(__name__, template_folder='templates')
	app.config.from_object(LocalDevelopmentConfig)

	db.init_app(app)

	app.app_context().push()
	db.create_all()
	return app

app = create_app()
from application.controllers import *

if __name__ == '__main__':
	# Turn sync to false to use without gdrive implementation & keys
	FLAG_gdrive = False
	if FLAG_gdrive:
		drive_service = auth('gcp_key.json', FLAG_gdrive)
	app.run(host='0.0.0.0', port=5000)