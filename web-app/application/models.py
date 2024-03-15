from application.database import db

class Teams(db.Model):
	__tablename__ = 'teams'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String, nullable=False, unique=True)
	name = db.Column(db.String, nullable=False)
	committee_pref = db.Column(db.Integer, nullable=False)
	size = db.Column(db.Integer, nullable=False)
	member_name_1 = db.Column(db.Integer, nullable=False)
	member_name_2 = db.Column(db.Integer, nullable=False)
	member_name_3 = db.Column(db.Integer, nullable=False)
	member_name_4 = db.Column(db.Integer, nullable=True)
