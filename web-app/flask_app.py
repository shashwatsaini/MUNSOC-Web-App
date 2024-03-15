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

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/events')
def events():
	return render_template('events.html')

@app.route('/the-secretariat')
def secretariat():
	return render_template('secretariat.html')

@app.route('/register')
def register():
	return render_template('register.html')

# from application.controllers import *

if __name__ == '__main__':
	app.run()