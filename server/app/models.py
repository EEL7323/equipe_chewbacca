from app import db
from passlib.apps import custom_app_context as pwd_context
import datetime

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	matricula = db.Column(db.String(64), unique=True)
	cardID = db.Column(db.String(64))
	password = db.Column(db.String(120))
	n_password = db.Column(db.String(64))
	registered_on = db.Column(db.DateTime)
	transactions = db.relationship('Transaction', backref='author', lazy='dynamic')
	
	def __init__(self, username, matricula, cardID):
		self.username = username
		self.matricula = matricula
		self.cardID = cardID
		self.registered_on = datetime.datetime.utcnow()
	
	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password,self.password)

	def hash_n_password(self, n_password):
		self.n_password = pwd_context.encrypt(self.matricula+n_password)

	def verify_n_password(self, matricula, n_password):
		return pwd_context.verify(matricula+n_password,self.n_password)

	def __str__(self):
		return '<User - Username:{self.username}, CardID:{self.cardID}, Matricula:{self.matricula}>'.format(**locals())

class Transaction(db.Model):
	__tablename__ = 'transaction'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = db.Column(db.DateTime)
	event_id = db.Column(db.Integer)
	
	def __str__(self):
		return "<Transaction - Type:{self.event_id}, UserID={self.user_id}>".format(**locals())


class Contador(db.Model):
	__tablename__ = 'contador'
	id = db.Column(db.Integer, primary_key=True)
	v = db.Column(db.Integer, index=True)
	timestamp = db.Column(db.DateTime)

	def __init__(self, v):
		self.v = v
		self.timestamp = datetime.datetime.utcnow()

	def __str__(self):
		return "<Contador - {self.v} at {self.timestamp}>".format(**locals())
