from flask import Flask
from flask import redirect, url_for, render_template
from application.config import LocalDevelopmentConfig

app = None

def create_app():
	app = Flask(__name__, template_folder='templates')
	app.config.from_object(LocalDevelopmentConfig)

	app.app_context().push()
	return app

app = create_app()
from application.controllers import *

if __name__ == '__main__':
	# app.run(host='0.0.0.0', port=5000)
	app.run()