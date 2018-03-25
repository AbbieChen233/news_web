#!/usr/bin/env python3
from flask import Flask,render_template
import os,json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELODE']=True


def readjson():
	file_json = {}
	strpath = "/home/shiyanlou/files"

	for path,d,filelist in os.walk(strpath):
		for filename in filelist:
			file_suffix = filename.split('.')
			
			if(file_suffix[1] == 'json'):
				absfilename = path + '/' + filename
				with open(absfilename,'r') as fopen:
					file_json[file_suffix[0]] = json.loads(fopen.read())
	return file_json

@app.route('/')
def index():
	file_json = readjson()
	return render_template('file.html',file_json=file_json)

@app.route('/files/<filename>')
def file(filename):

	file_json = readjson()
	strpath = "/home/shiyanlou/files"
	for path,d,filelist in os.walk(strpath):
		for _filename in filelist:
			absfilename = path + '/' + _filename
			if os.path.exists(absfilename):
				return render_template('index.html',file_json=file_json,filename=filename)
			else:
				return render_template('404.html'),400

