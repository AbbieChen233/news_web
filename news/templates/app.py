#!/usr/bin/env python3
from flask import Flask,render_template
import os,json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELODE']=True

@app.route('/')

			
def readjsonfile():
	filejson = {}
	strpath = "/home/shiyanlou/files"

	for path,d,filelist in os.walk(strpath):
		for filename in filelist:
			file_suffix = filename.split('.')
			
			if(file_suffix[1] == 'json'):
				absfilename = path + '/' + filename
				with open(absfilename,'r') as fopen:
					filejson[filename] = json.loads(fopen.read())
	return filejson

def index():
	file_json = {}
	file_json = readjsonfile()
	return render_template('file.html',file_json=file_json)

@app.route('/files/<filename>')
def file(filename):
	file_json = {}
	file_json = readjsonfile()

	strpath = "/home/shiyanlou/files"
	absfilename = strpath + '/' + filename + '.json'
	if os.path.exists(absfilename):
		return render_template('index.html',file_json=file_json,filename=filename)
	else:
		return render_template('404.html'),400
