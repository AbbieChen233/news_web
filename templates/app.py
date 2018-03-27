from flask import Flask,render_template, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELODE']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/blog'


db = SQLAlchemy(app)

client = MongoClient('127.0.0.1',27017)
mongdb = client.shiyanlou

class Category(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(80))
	
	def __init__(self,name):
		
		self.name = name
	def __repr__(self):
		return '<user %r>' % self.name

class File(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	title = db.Column(db.String(255))
	created_time = db.Column(db.DateTime)
	content = db.Column(db.Text)
	categery_id = db.Column(db.Integer,db.ForeignKey('category.id'))
	category = db.relationship('Category',backref=db.backref('files',lazy='dynamic'))
	

	def __init__(self,title,created_time,content,category):

		self.title = title
		self.created_time = created_time
		self.content = content
		self.category = category

	def add_tag(self,tag_name):
		tag_list = []
		tag_list = tags()

		if tag_name not in tag_list:
			tag_list.append(tag_name)
		mongdb.tags.update_one({'file_id':self.id,'tag':tag_list})

	def remove_tag(self,tag_name):
		tag_list = []
		tag_list = tags()
		if tag_name in tag_list:
			tag_list.remove(tag_name)

	
	
	def tags(self):
		tag_list = []
		tag = mongdb.tags.find_one({'file_id':self.id})
		if type(tag) == NoneType:
			mongdb.tags.insert_one({'file_id':self.id,'tag':[]})
		tag_list = tag['tag']
		return tag_list

		
	def __repr__(self):
		return '<user %r>' % self.title
		

all_file = File.query.all()


@app.route('/')
def index():
	for file in all_file:
		
    return render_template('index.html',all_file = all_file)
	
@app.route('/files/<file_id>')
def file(file_id):
	
    f =  File.query.filter_by(id=file_id).first()
    if f:
        return render_template('file.html', file=f)
    abort(404)
    

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404
