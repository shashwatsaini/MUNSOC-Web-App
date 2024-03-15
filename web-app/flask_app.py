import os
from flask import Flask
from flask import redirect, url_for, render_template
from application.config import LocalDevelopmentConfig
from application.database import db

current_dir = os.path.abspath(os.path.dirname(__file__))
app = None

def create_app():
	app = Flask(__name__, template_folder='templates')
	app.config.from_object(LocalDevelopmentConfig)

	db.init_app(app)

	app.app_context().push()
	return app

app = create_app()
from application.controllers import *

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)