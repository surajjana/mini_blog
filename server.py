from bottle import Bottle, run, route, static_file, request, response, template
from pymongo import MongoClient
from bson.json_util import dumps
import json
import pymongo
import requests
import time

app = Bottle(__name__)

client = MongoClient()

db = client.mini_blog

@app.hook('after_request')
def enable_cors():
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
	response.headers['Connection'] = 'keep-alive'

@app.route('/')
def root():
	return "<h1>Mini Blog Home</h1>"

@app.route('/admin')
def admin():
	return """
	<form action="/addArticle" method="get">
		<input type=text name=title placeholder=Title>
		<input type=text placeholder=Article>
		<input type=submit>
	</form>
	"""

@app.route('/addArticle')
def addArticle():
	title = request.form.body('title')

	cursor = db.articles.insert({"title": title})

	return "Success"

@app.route('/allArticles')
def allArticles():

	cursor = db.articles.find()

	articles = dumps(cursor)

	return articles