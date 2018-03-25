#!/usr/bin/env python3
from flask import Flask,render_template
from flask_sqlalchemy import SQLALchemy


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELODE']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/blog'


db = SQLALchemy(app)

class File(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	title = db.Column(db.String(255))
	created_time = db.Column(db.DateTime)
	categery_id = db.Column(db.Integer,db.Foreign('categery.id'))
	categery = db.relationship('Categery',backref=db.backref('files'))


	def __init__(self,title,created_time):
		self.title = title
		self.created_time = created_time
	def __repr__(self):
		return '<user %r>' % self.title

class Categery(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.Integer)
	
	def __init__(self,name):
		self.name = name
	def __repr__(self):
		return '<user %r>' % self.name

db.create_all()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/files/<filename>')
def file(filename):
	pass


	
