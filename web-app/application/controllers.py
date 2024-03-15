from flask import current_app as app
from flask import Flask, request
from flask import render_template, request, redirect, url_for
from application.database import db
from application.models import Teams

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/events')
def events():
	return render_template('events.html')

@app.route('/the-secretariat')
def secretariat():
	return render_template('secretariat.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
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

			db.session.add(team)
			db.session.commit()
			return render_template('register.html', registered=True)

		except Exception as e:
			print(e)
			return redirect('/')

