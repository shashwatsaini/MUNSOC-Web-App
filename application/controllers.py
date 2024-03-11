from flask import current_app as app
from flask import Flask, request
from flask import render_template, request, redirect, url_for

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/events')
def events():
	return render_template('events.html')