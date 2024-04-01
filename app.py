import os
import logging
from datetime import datetime
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

# Setup logging
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('webapp.log')
app.logger.addHandler(handler)

from application.controllers import *

if __name__ == '__main__':
	# Turn sync to false to use without gdrive implementation & keys
	FLAG_gdrive = True
	if FLAG_gdrive:
		drive_service = auth('gcp_key.json', FLAG_gdrive)
	app.logger.info(f'[{datetime.now()}] Web App Started')
	app.run(host='0.0.0.0', port=5000)